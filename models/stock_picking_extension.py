from odoo import models, fields,api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', 'in', allowed_company_ids)]"
    )


    @api.onchange('sale_id')
    def _onchange_sale_id(self):
        """ Si se cambia la orden de venta, sincroniza la cuenta analítica en las líneas de stock """
        if self.sale_id and self.sale_id.project_id:
            analytic_account = self.sale_id.project_id.analytic_account_id
            for move in self.move_lines:
                move.analytic_account_id = analytic_account
