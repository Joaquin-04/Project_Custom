from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', '=', company_id)]"
        )


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        """ Evita seleccionar un proyecto de otra empresa """
        for lead in self:
            if lead.project_id and lead.company_id and lead.project_id.company_id != lead.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ lead.project_id.name }' pertenece a otra empresa: { lead.project_id.company_id.name }."))



