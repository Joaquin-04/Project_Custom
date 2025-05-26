from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

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

    @api.model
    def default_get(self, fields_list):
        """Obtiene valores por defecto, como el nombre del lead si proviene de uno"""
        res = super(SaleOrder, self).default_get(fields_list)
        
        
        project_id = self.opportunity_id.project_id
        
        if project_id:
            res['project_id']=project_id

        return res


    


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
        """ Antes de confirmar la venta, abre un wizard para seleccionar o crear un proyecto """

        if self.opportunity_id:
            campos_faltantes = []
            for campo, descripcion in self.CAMPOS_OBLIGATORIOS.items():
                if not self.opportunity_id[campo]:  
                    campos_faltantes.append(f"⛔ {descripcion}")  # Agrega el icono rojo para mayor visibilidad
            
            if campos_faltantes:
                raise UserError("⚠️ Campos Obligatorios para el PROYECTO Vacíos en el Lead ⚠️\n\n"
                                "Los siguientes campos son obligatorios y están vacíos en el Lead:\n"
                                + "\n".join(campos_faltantes))

        
        if self.studio_almacen.id == 10:
            proyecto = self.env['project.project'].search([('name', '=', 'Gremio')], limit=1)
            _logger.warning(f"Buscando el proyecto: {proyecto}")
            if proyecto:
                self.project_id = proyecto.id
            else:
                raise UserError("No se encontró un proyecto con el nombre 'Gremio'.")

        if not self.project_id:
            return {

                'type': 'ir.actions.act_window',

                'res_model': 'sale.order.project.wizard',

                'view_mode': 'form',

                'target': 'new',

                'context': {'default_sale_order_id': self.id},

            }

        return super().action_confirm()
    

    
    def action_open_project_wizard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.project.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            }
        }



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





