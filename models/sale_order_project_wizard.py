from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrderProjectWizard(models.TransientModel):
    _name = 'sale.order.project.wizard'
    _description = 'Seleccionar o Crear Proyecto'

    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", required=True)

    company_id = fields.Many2one(
        'res.company', 
        string="Compañía",
        related='sale_order_id.company_id',
        readonly=True
    )
    
    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', '=', company_id)]"
    )

    
    create_new = fields.Boolean(string="Crear Nuevo Proyecto?", default=True)
    
    new_project_name = fields.Char(string="Nombre del Nuevo Proyecto")

    obra_padre_id = fields.Many2one(
        'project.project', 
        string="Obra Padre",
        domain="[('company_id', '=', company_id)]"
    )

    FIELDS_OPPORTUNITY=[
    
        'x_studio_nv_nombre_de_carga_obra',
        'x_studio_nv_direccion',
        'project_ubi_id',
        'cod_postal_proyect',
        'ubi_area_proyect',
        'ubi_code',
        'x_studio_celular_1'
        'x_studio_telefono_fijo',
        'phone_mobile_search',#fax1
        'estado_obra_proyect_id',
        'obratipo_proyect_id',
        'color_proyect_id',
        'lnart_proyect',
        'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'x_studio_nv_codigo_plus',
        'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'x_studio_nv_cartel',
        'provincia_id',
        'pais_cd'
    ]

    # En tu SaleOrderProjectWizard
    LEAD_TO_PROJECT_MAPPING = {
        # Campo Proyecto: Campo Lead
        'nombre_carga_obra': 'x_studio_nv_nombre_de_carga_obra',
        'direccion': 'x_studio_nv_direccion',
        'obratipo_ubi': 'project_ubi_id',
        'cod_postal_proyect': 'cod_postal_proyect',
        'ubi_area_proyect': 'ubi_area_proyect',
        'celular_1': 'x_studio_celular_1',
        'telefono_fijo': 'x_studio_telefono_fijo',
        'fax_1': 'phone_mobile_search',  # Asumiendo que phone_mobile_search es el fax1
        'estado_obra_proyect': 'estado_obra_proyect_id',
        'obratipo_proyect': 'obratipo_proyect_id',
        'color_proyect': 'color_proyect_id',
        'lnart_proyect': 'lnart_proyect_id',
        'fecha_pactada_entrega': 'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'codigo_plus': 'x_studio_nv_codigo_plus',
        'cartel_obra_id': 'cartel_obra_id',
        'provincia_id': 'provincia_id',
        'pais_cd': 'pais_cd',
        'kg_perfileria': 'x_studio_nv_kg_perfilera',
        # Agrega más mapeos según necesidad
    }


    @api.model
    def default_get(self, fields_list):
        """Obtiene valores por defecto, como el nombre del lead si proviene de uno"""
        res = super(SaleOrderProjectWizard, self).default_get(fields_list)
        sale_order = self.env['sale.order'].browse(self.env.context.get('default_sale_order_id'))

        lead = sale_order.opportunity_id

        project_id = sale_order.opportunity_id.project_id
        
        if project_id:
            res['project_id']=project_id
        
        if sale_order.opportunity_id:  # Si la orden proviene de un lead
            res['new_project_name'] = sale_order.opportunity_id.name

        return res

    @api.constrains('create_new', 'project_id')
    def _check_project_selection(self):
        """Valida que si no se crea un nuevo proyecto, el campo project_id no esté vacío"""
        for wizard in self:
            if not wizard.create_new and not wizard.project_id:
                raise ValidationError(_("Debe seleccionar un proyecto si no va a crear uno nuevo."))


    

    def action_apply(self):
        """ Aplica la selección del proyecto o crea uno nuevo con validaciones"""
        if self.create_new:
            if not self.new_project_name:
                raise UserError(_("Debe ingresar un nombre para el nuevo proyecto."))

            project = self.env['project.project'].create({
                'name': self.new_project_name,
                'company_id': self.sale_order_id.company_id.id,
                'obra_padre_id': self.obra_padre_id.id if self.obra_padre_id else False,
            })

            if self.obra_padre_id:
                    # Copiar campos del padre
                    project._onchange_obra_padre_id()
            else:
                # Copiar campos desde el CRM lead si existe
                sale_order = self.env['sale.order'].browse(self.env.context.get('default_sale_order_id'))
                opportunity = sale_order.opportunity_id
                if opportunity:
                    self._copy_fields_from_opportunity(project, opportunity, project.FIELDS_TO_INCLUDE)
                    # Copiar campos adicionales específicos
                    project.obra_vend_cd = opportunity.vendedor_id
                    project.obra_jefe_cd = opportunity.jefe_obra_id
                    #project.obra_tec_cd = opportunity.cotizador_id  # Asumiendo relación
                    #project.tiene_colocacion = 'S' if opportunity.probability > 50 else 'N'
                    
                    # Para campos computados que son stored=True
                    if opportunity.ubi_code:
                        project.ubi_code = opportunity.ubi_code
           
        else:
            project = self.project_id

        # Asignar el proyecto a la orden de venta
        self.sale_order_id.project_id = project
        #self.sale_order_id._onchange_project_id()

        # Forzar actualización de líneas
        self.sale_order_id._update_analytic_distribution()

        #Confirmar la orden de venta
        self.sale_order_id.action_confirm()

        return {'type': 'ir.actions.act_window_close'}

    

    def _copy_fields_from_opportunity(self, project, opportunity, fields_to_include):
        """Copia campos desde el lead al proyecto usando el mapeo definido"""
        for project_field, lead_field in self.LEAD_TO_PROJECT_MAPPING.items():
            try:
                if project_field not in fields_to_include:
                    continue
                    
                if not opportunity[lead_field]:
                    continue  # No copiar valores vacíos
                    
                field_type = project._fields[project_field].type
                
                # Manejo especial para tipos de campos
                if field_type == 'many2one':
                    project[project_field] = opportunity[lead_field].id
                elif field_type == 'many2many':
                    project[project_field] = [(6, 0, opportunity[lead_field].ids)]
                elif field_type == 'date' and not opportunity[lead_field]:
                    continue  # Saltar fechas inválidas
                else:
                    project[project_field] = opportunity[lead_field]
                    
            except Exception as e:
                _logger.error(f"Error copiando {lead_field} a {project_field}: {str(e)}")
                continue


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        for record in self:
            if record.project_id and record.company_id != record.project_id.company_id:
                raise ValidationError(_(
                    f"El proyecto seleccionado '{record.project_id.name}' pertenece a otra empresa: {record.project_id.company_id.name}."
                ))





