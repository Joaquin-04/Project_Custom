from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ProjectObraTipo(models.Model):
    _name = 'project.obratipo'  # Nombre técnico del modelo
    _description = 'Obra Tipo'  # Descripción del modelo
    _sql_constraints = [
        ('cod_unique', 'unique (cod)', 'El código debe ser único.')
    ]

    cod = fields.Char(string='ObraTpCd', required=True)
    name = fields.Char(string='ObraTpDesc', required=True)
    descripcion = fields.Char(string='ObraTpCrc', required=False)







    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('cod', operator, name), ('name', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {name} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn



    def _compute_display_name(self):
        for record in self:
            if record.cod:
                record.display_name = f"[{record.cod}] {record.name}"
            else:
                record.display_name = record.name