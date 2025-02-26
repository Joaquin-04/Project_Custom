from odoo import models, fields, api
from odoo.exceptions import ValidationError



class ProjectObraEstado(models.Model):
    _name = 'project.obraestado'  # Nombre técnico del modelo
    _description = 'Obra estado'  # Descripción del modelo
    _sql_constraints = [
        ('cod_unique', 'unique (cod)', 'El código debe ser único.')
    ]

    cod = fields.Integer(string='cod', required=True)
    name = fields.Char(string='obraestado', required=True)
    obra_estado_color = fields.Char(string='Estado Color', required=False)
    obraCrc = fields.Integer(string='Estado Crc', required=False)






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


