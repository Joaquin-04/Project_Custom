from odoo import models, fields,api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', 'in', allowed_company_ids)]",
        #compute="_compute_project_id",
        readonly=False
    )

    


