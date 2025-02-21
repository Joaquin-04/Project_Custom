from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectColor(models.Model):
    _name = 'project.color'  # Nombre técnico del modelo
    _description = 'Color de proyecto'  # Descripción del modelo
    _sql_constraints = [
        ('cod_unique', 'unique (cod)', 'El código debe ser único.')
    ]

    cod = fields.Integer(string='ColoCd', required=True)
    name = fields.Char(string='ColoNm', required=True)
    descripcion = fields.Integer(string='ColoCrc', required=True)

    @api.constrains('cod')
    def _check_unique_cod(self):
        for record in self:
            if self.search([('cod', '=', record.cod), ('id', '!=', record.id)]):
                raise ValidationError("El código debe ser único.")







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