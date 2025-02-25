from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
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



    def write(self, vals):
        _logger.warning("Write!!!")
        _logger.warning(f"valores: {vals}")
        
        if 'project_id' in vals:
            if vals['project_id']:
                # Se ha asignado un proyecto, obtenemos su información
                project = self.env['project.project'].browse(vals['project_id'])
                if project:
                    new_vals = {}
                    if project.obra_nr:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = project.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = False
                    if project.obra_padre_id:
                        new_vals['x_studio_nv_numero_de_sp'] = project.obra_padre_id.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_sp'] = False
                    vals.update(new_vals)
            else:
                # Se está borrando el proyecto, establecemos los campos en 0 o False
                vals.update({
                    'x_studio_nv_numero_de_obra_relacionada': 0,
                    'x_studio_nv_numero_de_sp': 0,
                })
        return super(CrmLead, self).write(vals)



