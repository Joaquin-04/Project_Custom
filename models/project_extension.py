from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    obra_nr = fields.Char(string="Número de Obra", readonly=True, copy=False)
    
    obra_padre_id = fields.Many2one(
        'project.project',
        string="Obra Padre",
        domain="[('company_id', 'in', allowed_company_ids)]",  # Filtra por compañías permitidas
    )


    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.obra_nr}] {record.name}" if record.obra_nr else record.name

    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """ Permite buscar proyectos por 'obra_nr' y 'name' en cualquier parte del sistema """
        args = args or []
        if name:
            domain = ['|', ('obra_nr', operator, name), ('name', operator, name)]
        else:
            domain = []
        return super(ProjectProject, self).name_search(name, domain + args, operator, limit)
    

    @api.model
    def create(self, vals):
        # Asignar la compañía si no se proporcionó
        if not vals.get('company_id'):
            vals['company_id'] = self.env.company.id

        
        # Generar número de obra secuencial
        if not vals.get('obra_nr'):
            next_value= self.env['ir.sequence'].next_by_code('custom.project.number')
            #_logger.warning(f"next_value: {next_value}")

            vals['obra_nr'] = next_value
        
        # Crear cuenta analítica automáticamente
        if not vals.get('analytic_account_id'):
            analytic_account = self.env['account.analytic.account'].create({
                'name': vals.get('name'),
                'company_id': self.company_id.id,
                'plan_id': 1,
            })
            vals['analytic_account_id'] = analytic_account.id
        
        return super(ProjectProject, self).create(vals)
        
