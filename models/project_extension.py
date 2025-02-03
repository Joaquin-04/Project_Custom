from odoo import models, fields, api, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    obra_nr = fields.Char(string="Número de Obra", readonly=True, copy=False)
    obra_padre_id = fields.Many2one('project.project', string="Obra Padre", 
                                    domain="[('obra_nr', '!=', False)]")
    obra_tp_cd = fields.Selection([
        ('residential', 'Residencial'),
        ('commercial', 'Comercial'),
        ('infrastructure', 'Infraestructura'),
    ], string="Tipo de Obra")

    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        domain = args + ['|', ('obra_nr', operator, name), ('name', operator, name)]
        return super(ProjectProject, self).name_search(name, domain, operator, limit)
    

    @api.model
    def create(self, vals):
        # Generar número de obra secuencial
        if not vals.get('obra_nr'):
            vals['obra_nr'] = self.env['ir.sequence'].next_by_code('custom.project.number')
        
        # Crear cuenta analítica automáticamente
        if not vals.get('analytic_account_id'):
            analytic_account = self.env['account.analytic.account'].create({
                'name': vals.get('name'),
                'company_id': self.company_id.id,
            })
            vals['analytic_account_id'] = analytic_account.id
        
        return super(ProjectProject, self).create(vals)
        
