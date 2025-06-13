# models/analytic_account.py
from odoo import models, fields, api

class AnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    obra_nr = fields.Char(
        string="Número de Obra",
        compute="_compute_obra_nr",
        store=True,
        readonly=True,
        copy=False,
        size=5,
        tracking=True
    )

    @api.depends('project_ids.obra_nr')
    def _compute_obra_nr(self):
        for record in self:
            if record.project_ids:
                # Tomar el primer proyecto ordenado por ID (el más antiguo)
                record.obra_nr = record.project_ids.sorted(key='id')[0].obra_nr
            else:
                record.obra_nr = False

    def _compute_display_name(self):
        for record in self:
            if record.obra_nr:
                record.display_name = f"[{record.obra_nr}] {record.name}"
            else:
                record.display_name = record.name
                

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

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


