from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ubic(models.Model):
    _name = 'project.ubic'  # Nombre técnico del modelo
    _description = 'Ubicación'  # Descripción del modelo
    _sql_constraints = [
        ('ubic_cd_unique', 'unique (ubic_cd)', 'El código de ubicación debe ser único.'),
        ('ubic_nm_unique', 'unique (ubic_nm)', 'El nombre de ubicación debe ser único.')
    ]

    # Campos del modelo
    ubic_cd = fields.Integer(string='UbicCd', required=True)  # Código de ubicación (único y requerido)
    ubic_nm = fields.Char(string='UbicNm', required=True)  # Nombre de ubicación (único y requerido)
    ubic_nm_tt = fields.Char(string='UbicNmTt', required=False)  # Nombre completo de ubicación
    ubic_usable = fields.Char(string='UbicUsable', default=True)  # Ubicación usable (por defecto True)
    ubic_cp = fields.Char(string='UbicCP', required=False)  # Código postal
    ubic_area_cd = fields.Char(string='UbicAreaCd', required=False)  # Código de área
    ubic_crc = fields.Char(string='UbicCrc', required=False)  # CRC
    ubic_dist_a_fabr = fields.Char(string='UbicDistAFabr', required=False)  # Distancia a fábrica

    # Búsqueda por 'name' o 'cod' en campos Many2one
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'code' en campos Many2one."""

        if domain is None:
            domain = []  # Si domain es None, lo inicializamos como una lista vacía

        if name:
            # Agregar condiciones de búsqueda (ubic_cd o ubic_nm)
            domain = ['|', ('ubic_cd', operator, name), ('ubic_nm', operator, name)] + domain

        # Ejecutar la búsqueda
        return self._search(domain, limit=limit, order=order)

    # Método para calcular el nombre mostrado (display_name)
    def _compute_display_name(self):
        for record in self:
            if record.ubic_cd:
                record.display_name = f"[{record.ubic_cd}] {record.ubic_nm}"
            else:
                record.display_name = record.ubic_nm