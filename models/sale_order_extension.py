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


    @api.onchange('project_id')
    def _onchange_project_id(self):
        _logger.warning(f"_onchange_project_id")
        """ Al cambiar el proyecto, actualiza la cuenta analítica en todas las líneas de venta """
        if self.project_id:
            analytic_account = self.project_id.analytic_account_id
            _logger.warning(f"analytic_account: {analytic_account}")
            for line in self.order_line:
                line.analytic_distribution = analytic_account


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





