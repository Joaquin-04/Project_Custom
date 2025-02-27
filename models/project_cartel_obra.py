from odoo import models, fields,api
from odoo.exceptions import ValidationError


class ProjectCartelObra(models.Model):
    _name = 'project.cartel.obra'
    _description = 'Opciones para Cartel de Obra'

    name = fields.Char(string="Opción", required=True)

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search([('name', '=', record.name), ('id', '!=', record.id)]):
                raise ValidationError("El nombre debe ser único.")