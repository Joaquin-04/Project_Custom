from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one('project.project', string="Proyecto")
