from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    obra_nr = fields.Char(string="Número de Obra", readonly=False, copy=False,store=True)
    
    obra_padre_id = fields.Many2one(
        'project.project',
        string="Obra Padre",
        domain="[('company_id', 'in', allowed_company_ids)]",  # Filtra por compañías permitidas
        no_create=True
    )


    def _compute_display_name(self):
        for record in self:
            if record.obra_nr:
                record.display_name = f"[{record.obra_nr}] {record.name}"
            else:
                record.display_name = record.name

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'obra_nr' en campos Many2one."""

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('obra_nr', operator, name), ('name', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {name} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn
        

    

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
        
