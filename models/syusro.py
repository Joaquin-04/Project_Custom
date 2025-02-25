from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectSyusro(models.Model):
    _name = 'project.syusro'
    _description = 'Gestión de SYUSRO (Usuarios para Proyectos)'

    syusro_cd = fields.Integer(string="Código", required=True)
    syusro_nm = fields.Char(string="Nombre", required=True)
    syusro_rol = fields.Char(string="Rol")
    syusro_fc_alta = fields.Date(string="Fecha de Alta")

    _sql_constraints = [
        ('syusro_cd_unique', 'unique(syusro_cd)', 'El código debe ser único.')
    ]

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('syusro_cd', operator, name), ('syusro_nm', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {syusro_nm} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn



    def _compute_display_name(self):
        for record in self:
            if record.syusro_cd:
                record.display_name = f"[{record.syusro_cd}] {record.syusro_nm}"
            else:
                record.display_name = record.syusro_nm





