from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        tracking=True
    )
    studio_almacen = fields.Many2one(
        'stock.warehouse', 
        string="Almacén",
        tracking=True
    )

    CAMPOS_OBLIGATORIOS = {
        #'x_studio_nv_nombre_de_carga_obra': "NV Nombre de carga obra",
        'obratipo_proyect_id': "NV Tipo",
        'lnart_proyect_id': "NV Línea",
        'color_proyect_id': "NV Color",
        'x_studio_nv_codigo_plus': "NV Código Plus",
        'x_studio_nv_direccion': "NV Dirección",
        'x_studio_nv_fecha_probable_de_entrega_de_obra': "NV Fecha probable de entrega de obra",
        'cartel_obra_id': "NV Cartel",
    }
    
    LEAD_PARENT_SELECTION_MAPPING = {
        'color_proyect': {
            'lead_field': 'color_proyect_id',  # Campo en el CRM lead
            'parent_field': 'color_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'lnart_proyect': {
            'lead_field': 'lnart_proyect_id',  # Campo en el CRM lead
            'parent_field': 'lnart_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obratipo_proyect': {
            'lead_field': 'obratipo_proyect_id',  # Campo en el CRM lead
            'parent_field': 'obratipo_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obratipo_ubi': {
            'lead_field': 'project_ubi_id',  # Campo en el CRM lead
            'parent_field': 'obratipo_ubi',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'direccion': {
            'lead_field': 'x_studio_nv_direccion',  # Campo en el CRM lead
            'parent_field': 'direccion',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'telefono_fijo': {
            'lead_field': 'x_studio_telefono_fijo',  # Campo en el CRM lead
            'parent_field': 'telefono_fijo',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'celular_1': {
            'lead_field': 'x_studio_celular_1',  # Campo en el CRM lead
            'parent_field': 'celular_1',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fax_1': {
            'lead_field': 'x_studio_fax1',  # Campo en el CRM lead
            'parent_field': 'fax_1',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fax_2': {
            'lead_field': 'x_studio_fax2',  # Campo en el CRM lead
            'parent_field': 'fax_2',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'codigo_plus': {
            'lead_field': 'x_studio_nv_codigo_plus',  # Campo en el CRM lead
            'parent_field': 'codigo_plus',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fecha_pactada_entrega': {
            'lead_field': 'x_studio_nv_fecha_probable_de_entrega_de_obra',  # Campo en el CRM lead
            'parent_field': 'fecha_pactada_entrega',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },
        'fecha_renegociada_entrega': {
            'lead_field': 'x_studio_nv_fecha_probable_de_entrega_de_obra',  # Campo en el CRM lead
            'parent_field': 'fecha_renegociada_entrega',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },
        'obra_vend_cd': {
            'lead_field': 'vendedor_id',  # Campo en el CRM lead
            'parent_field': 'obra_vend_cd',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obra_jefe_cd': {
            'lead_field': 'jefe_obra_id',  # Campo en el CRM lead
            'parent_field': 'obra_jefe_cd',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'cartel_obra_id': {
            'lead_field': 'cartel_obra_id',  # Campo en el CRM lead
            'parent_field': 'cartel_obra_id',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'provincia_id': {
            'lead_field': 'provincia_id',  # Campo en el CRM lead
            'parent_field': 'provincia_id',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'kg_perfileria': {
            'lead_field': 'x_studio_nv_kg_perfilera',  # Campo en el CRM lead
            'parent_field': 'kg_perfileria',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },     
    }

    


    


    def _update_analytic_distribution(self,reset=False):
        """Actualiza la distribución analítica en todas las líneas"""
        if not reset:
            if self.project_id and self.project_id.analytic_account_id:
                analytic_account_id = self.project_id.analytic_account_id.id
                distribution = {str(analytic_account_id): 100.0}
                
                for line in self.order_line:
                    if line.display_type not in ('line_section', 'line_note'):
                        line.analytic_distribution = distribution

        else:
            for line in self.order_line:
                    if line.display_type not in ('line_section', 'line_note'):
                        line.analytic_distribution = False
            

    


    """
    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        #Evita seleccionar un proyecto de otra empresa
        for order in self:
            if order.project_id and order.company_id and order.project_id.company_id != order.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ order.project_id.name }' pertenece a otra empresa: { order.project_id.company_id.name }."))
    """

    
    

    def action_confirm(self):
        """Confirmación automática con creación de proyecto si no existe"""
        

        if self.opportunity_id.stage_id.id != 41:
            raise UserError("Primero ponga el lead en el estado 1401")

        # Verificación de campos obligatorios en el lead (existente)
        if self.opportunity_id:
            campos_faltantes = []
            for campo, descripcion in self.CAMPOS_OBLIGATORIOS.items():
                if not self.opportunity_id[campo]:  
                    campos_faltantes.append(f"⛔ {descripcion}")  # Agrega el icono rojo para mayor visibilidad
            
            if campos_faltantes:
                raise UserError("⚠️ Campos Obligatorios para el PROYECTO Vacíos en el Lead ⚠️\n\n"
                                "Los siguientes campos son obligatorios y están vacíos en el Lead:\n"
                                + "\n".join(campos_faltantes))

        

        
        # Lógica especial para almacén Gremio
        if self.studio_almacen.id == 10:
            proyecto = self.env['project.project'].search([('name', '=', 'Gremio')], limit=1)
            _logger.warning(f"Buscando el proyecto: {proyecto}")
            if proyecto:
                self.project_id = proyecto.id
            else:
                raise UserError("No se encontró un proyecto con el nombre 'Gremio'.")

        # Creación automática de proyecto si no existe
        if not self.project_id and self.opportunity_id:
            try:
                if not self.opportunity_id.name:
                    raise UserError(_("Debe ingresar un nombre para el nuevo proyecto."))
                
                # 1. Crear proyecto base
                new_project = self.env['project.project'].create({
                    'name': self.opportunity_id.name,
                    'company_id': self.company_id.id,
                    'obra_padre_id': self.opportunity_id.obra_padre_id.id if self.opportunity_id.obra_padre_id else False,
                })

                if not new_project.obra_padre_id:
                    #si no tiene obra padre quiere decir que esta obra (proyecto) es padre
                    new_project.obra_padre_nr=new_project.obra_nr


                # 2. Copiar campos desde el lead usando los mapeos del wizard
                lead = self.opportunity_id
                
                
                self._apply_lead_vs_parent_field(new_project, lead, self.LEAD_PARENT_SELECTION_MAPPING)
                    

                # 4. Vincular proyecto a orden y lead
                self.project_id = new_project
                self.x_studio_nv_numero_de_obra_padre = new_project.obra_padre_nr
                self.x_studio_nv_numero_de_obra_relacionada = new_project.obra_nr
                self.opportunity_id.project_id = new_project
                if new_project.obra_padre_id:
                    self.opportunity_id.obra_padre_id = new_project.obra_padre_id
                else:
                    self.opportunity_id.obra_padre_id = new_project
                self.opportunity_id.x_studio_nv_numero_de_obra_relacionada = new_project.obra_nr
                self.opportunity_id.x_studio_nv_numero_de_sp = new_project.obra_padre_nr
                
                # 5. Actualizar distribución analítica
                self._update_analytic_distribution()

            except Exception as e:
                # Registrar el log de auditoría para errores
                audit_vals = {
                    'project_id': 0,
                    'user_id': self.env.uid,
                    'company_id': self.company_id.id,
                    'state': 'error',
                    'message': f'Error en action_apply: {str(e)}'
                }
                self.env['project.sequence.log'].sudo().create(audit_vals)
                error_msg = f"Error creando proyecto automático: {str(e)}"
                _logger.error(error_msg)
                raise UserError(_(error_msg))
                

        return super().action_confirm()
    

    def _apply_lead_vs_parent_field(self, project, opportunity, field_mapping):
        """
        Aplica la lógica de selección entre el valor del lead y el del proyecto padre.
        
        field_mapping: dict donde cada clave es un campo del proyecto y su valor es un dict con:
            - lead_field: nombre del campo en el CRM lead.
            - parent_field: nombre del campo en el proyecto padre (opcional).
            - priority: 'lead' (usar siempre el valor del lead si existe) o 'parent_if_empty' (usar el del padre si el lead está vacío).
        
        Para el caso del teléfono (campo 'telefono_fijo'), se prioriza el valor del lead; si está vacío,
        se usa el valor del cliente (partner_id.phone).
        
        Lógica avanzada de prioridad de campos:
        1. Determina fuente de datos (lead/padre)
        2. Aplica reglas de prioridad configuradas
        3. Genera logs detallados de asignación
        
        Casos Especiales:
        - Campos telefónicos con fallback a partner
        - Campos obligatorios (strict_lead)
        - Formateo de valores para logs
        """

        # Justo antes de asignar el valor al proyecto:
        
        
        
        # Función para formatear valores
        def format_value(value):
            if isinstance(value, models.BaseModel):
                return f"(ID: {value.id}, Nombre: {value.display_name})" if value else "None"
            elif isinstance(value, bool):
                return str(bool(value))
            elif value is None:
                return "None"
            return str(value)

        
        parent_project = project.obra_padre_id
        #_logger.warning(f"proyecto {project.name} \n padre {parent_project.name}")
        
        for proj_field, config in field_mapping.items():
            # Sanitizar campos telefónicos (NUEVO CÓDIGO)
            
                
            # Caso especial para el campo teléfono
            if proj_field == 'celular_1':
                # Intentar obtener el valor del lead
                lead_value = getattr(opportunity, config.get('lead_field'), False)
                # Si no hay valor en el lead, intentamos tomarlo del teléfono del cliente (partner_id.phone)
                if not lead_value and opportunity.partner_id:
                    lead_value = opportunity.partner_id.phone
                # Si hay un proyecto padre y el lead no tiene valor, obtenemos el valor del padre
                if parent_project:
                    parent_value = parent_project and config.get('parent_field') and getattr(parent_project, config.get('parent_field'), False) or False
                else:
                    parent_value = False
                # Según la prioridad, se asigna
                if config.get('priority', 'lead') == 'lead':
                    value = lead_value if lead_value else parent_value
                else:
                    value = parent_value if parent_value else lead_value
            else:
                # Lógica por defecto para otros campos
                lead_value = getattr(opportunity, config.get('lead_field'), False)

                if parent_project:
                    parent_value = parent_project and config.get('parent_field') and getattr(parent_project, config.get('parent_field'), False) or False
                else:
                    parent_value = False
                # Nueva lógica para prioridad estricta del lead
                if config.get('priority') == 'strict_lead':
                    value = lead_value  # Toma el valor del lead incluso si está vacío
                    source = 'LEAD (forzado)'
                    final_value = lead_value
            
                elif config.get('priority', 'lead') == 'lead':
                    value = lead_value if lead_value else parent_value
                    source = 'LEAD' if lead_value else 'PADRE (por vacío LEAD)'
                    final_value = lead_value or parent_value
                
                else:
                    value = parent_value if parent_value else lead_value
                    source = 'PADRE' if parent_value else 'LEAD (por vacío PADRE)'
                    final_value = parent_value or lead_value

            # Log detallado
            _logger.warning(
                "\n| Campo Proyecto: %s"
                "\n| Fuente: %s"
                "\n| Valor LEAD (%s): %s"
                "\n| Valor PADRE (%s): %s"
                "\n| Valor FINAL asignado: %s"
                "\n|----------------------------------",
                proj_field.upper(),
                source,
                config.get('lead_field', 'N/A'),
                format_value(lead_value),
                config.get('parent_field', 'N/A'),
                format_value(parent_value),
                format_value(final_value)
            )


            if proj_field in ['celular_1', 'telefono_fijo', 'fax_1', 'fax_2']:
                value = self._sanitize_phone(value)
                
            project[proj_field] = value


    
    def _sanitize_phone(self, value):
        """Remueve todos los caracteres no numéricos de un string."""
        if value and isinstance(value, str):
            return re.sub(r'[^\d]', '', value)
        return value
    
    



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        """Hereda distribución analítica al crear línea"""
        if 'order_id' in vals:
            order = self.env['sale.order'].browse(vals['order_id'])
            if order.project_id and order.project_id.analytic_account_id:
                analytic_account_id = order.project_id.analytic_account_id.id
                vals.setdefault('analytic_distribution', {str(analytic_account_id): 100.0})
        return super().create(vals)





