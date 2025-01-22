from odoo import models, fields, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    next_project_number = fields.Integer(
        string="Siguiente Número de Obra",
        config_parameter="custom_project_management.next_project_number",
        default=20000,
    )

    @api.model
    def set_values(self):
        super().set_values()
        sequence = self.env['ir.sequence'].search([('code', '=', 'custom.project.number')], limit=1)
        if sequence:
            sequence.write({'number_next': self.next_project_number})
