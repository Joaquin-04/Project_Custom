from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ChangeObraNrWizard(models.TransientModel):
    _name = 'change.obra.nr.wizard'
    _description = "Wizard para cambiar el número de obra"

    new_obra_nr = fields.Char('Nuevo Número de Obra', required=True, size=5)

    def action_change_obra_nr(self):
        project_id = self.env.context.get('active_id')
        if not project_id:
            raise ValidationError(_("No se encontró el proyecto activo."))

        project = self.env['project.project'].browse(project_id)
        # Validar que el nuevo número no esté en uso en otro proyecto
        existing = self.env['project.project'].search([
            ('obra_nr', '=', self.new_obra_nr),
            ('id', '!=', project.id)
        ], limit=1)
        if existing:
            raise ValidationError(_("El número de obra ya existe. Por favor, elija otro."))

        # Actualizar el número de obra
        project.write({'obra_nr': self.new_obra_nr})
        return {'type': 'ir.actions.act_window_close'}
