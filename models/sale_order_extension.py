from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

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

    @api.model
    def default_get(self, fields_list):
        """Obtiene valores por defecto, como el nombre del lead si proviene de uno"""
        res = super(SaleOrder, self).default_get(fields_list)
        
        
        project_id = self.opportunity_id.project_id
        
        if project_id:
            res['project_id']=project_id

        return res


    
    def write(self, vals):
        _logger.warning("Write!!!")
        _logger.warning(f"valores: {vals}")
        
        # Ejecutar primero la escritura normal para tener los últimos valores
        result = super(SaleOrder, self).write(vals)
        
        if 'project_id' in vals:
            project = None
            if vals['project_id']:
                # Se ha asignado un proyecto, obtenemos su información
                project = self.env['project.project'].browse(vals['project_id'])
                
                # Actualizar reservas de material
                for reservation in self.material_reservation_ids:
                    reservation.stage_id = False
                
                # Actualizar campos personalizados
                new_vals = {}
                if project.obra_nr:
                    new_vals['x_studio_nv_numero_de_obra_relacionada'] = project.obra_nr
                else:
                    new_vals['x_studio_nv_numero_de_obra_relacionada'] = False
                
                if project.obra_padre_id:
                    new_vals['x_studio_nv_numero_de_obra_padre'] = project.obra_padre_id.obra_nr
                else:
                    new_vals['x_studio_nv_numero_de_obra_padre'] = False
                
                self.write(new_vals)  # Actualizar campos sin entrar en recursión
                
                # Actualizar distribución analítica después de confirmar cambios
                self._update_analytic_distribution()
            else:
                # Limpiar distribución analítica si se quita el proyecto
                self._update_analytic_distribution(reset=True)
                # Limpiar campos si se quita el proyecto
                self.write({
                    'x_studio_nv_numero_de_obra_relacionada': 0,
                    'x_studio_nv_numero_de_obra_padre': 0,
                })
        
        return result


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
            

    


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        """ Evita seleccionar un proyecto de otra empresa """
        for order in self:
            if order.project_id and order.company_id and order.project_id.company_id != order.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ order.project_id.name }' pertenece a otra empresa: { order.project_id.company_id.name }."))


    
    

    def action_confirm(self):
        """ Antes de confirmar la venta, abre un wizard para seleccionar o crear un proyecto """

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





