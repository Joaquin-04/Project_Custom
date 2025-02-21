from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class ProjectProvincia(models.Model):
    _name = 'project.provincia'
    _description = 'Provincias'

    pais_cd = fields.Char(string="Código de País", required=True, unique=True)
    prvn_cd = fields.Char(string="Código de Provincia", required=True, unique=True)
    prvn_nm = fields.Char(string="Nombre de Provincia", required=True)
    pais_prvn_crc = fields.Char(string="Código de Representación", required=False)

    _sql_constraints = [
    
        ('prvn_cd_unique', 'unique(prvn_cd)', '¡El código de provincia debe ser único!'),
    ]

    @api.constrains('pais_cd', 'prvn_cd')
    def _check_unique_codes(self):
        for record in self:
            if record.prvn_cd:
                existing_provincia = self.search([
                    ('prvn_cd', '=', record.prvn_cd),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_provincia:
                    raise ValidationError(f"¡El código de provincia {record.prvn_cd} ya existe!")

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.pais_cd}-{record.prvn_cd}] {record.prvn_nm}"

    @api.model
    def create(self, vals):
        if not vals.get('pais_cd') or not vals.get('prvn_cd'):
            raise ValidationError("Debe ingresar un código de país y un código de provincia.")
        return super(ProjectProvincia, self).create(vals)




    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('prvn_cd', operator, name), ('prvn_nm', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {name} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn



    def _compute_display_name(self):
        for record in self:
            if record.prvn_cd:
                record.display_name = f"[{record.prvn_cd}] {record.prvn_nm}"
            else:
                record.display_name = record.prvn_nm




















