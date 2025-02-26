from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
    )


    
    def write(self, vals):
        _logger.warning("Write!!!")
        _logger.warning(f"valores: {vals}")
        
        if 'project_id' in vals:
            if vals['project_id']:
                # Se ha asignado un proyecto, obtenemos su información
                project = self.env['project.project'].browse(vals['project_id'])

                # Actualiza la cuenta analítica en las líneas de venta
                if self.project_id.analytic_account_id:
                    analytic_account_id = project.analytic_account_id.id
                    distribution = {str(analytic_account_id): 100.0}
                    _logger.warning(f"analytic_account_id: {analytic_account_id} \n distribution: {distribution}")
                    
                    # Versión compatible con Odoo 16+
                    for line in self.order_line:
                        if line.display_type not in ('line_section', 'line_note'):
                            line.update({
                                'analytic_distribution': distribution,
                                # Si necesitas mantener compatibilidad con campos antiguos
                                #'analytic_account_id': analytic_account.id
                            })

                
                for reservation in self.material_reservation_ids:
                    reservation.stage_id = False  # Vacía la etapa cuando cambia el número de proyecto
                
                
                if project:
                    new_vals = {}
                    if project.obra_nr:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = project.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = False
                    if project.obra_padre_id:
                        new_vals['x_studio_nv_numero_de_obra_padre'] = project.obra_padre_id.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_obra_padre'] = False
                    vals.update(new_vals)
            else:
                # Se está borrando el proyecto, establecemos los campos en 0 o False
                vals.update({
                    'x_studio_nv_numero_de_obra_relacionada': 0,
                    'x_studio_nv_numero_de_obra_padre': 0,
                })
        return super(SaleOrder, self).write(vals)


    """
    
    """



    


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        """ Evita seleccionar un proyecto de otra empresa """
        for order in self:
            if order.project_id and order.company_id and order.project_id.company_id != order.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ order.project_id.name }' pertenece a otra empresa: { order.project_id.company_id.name }."))


    
    def action_confirm(self):
        """ Antes de confirmar la venta, abre un wizard para seleccionar o crear un proyecto """
        if not self.project_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.project.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_sale_order_id': self.id,
                    'default_sale_company_id':self.company_id
                },
            }
        return super().action_confirm()





