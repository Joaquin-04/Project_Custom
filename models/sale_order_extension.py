from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', 'in', allowed_company_ids)]"
    )