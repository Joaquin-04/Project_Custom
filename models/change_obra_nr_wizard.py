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
        
        # El numero de la obra padre sera igual al numero de obra
        project['obra_padre_nr'] = project.obra_nr

        # Si el proyecto tiene obra padre entonces toma el numero de obra de la obra padre
        if project.obra_padre_id:
            project['obra_padre_nr'] = project.obra_padre_id.obra_nr

        # Actualizar el campo en las órdenes de venta relacionadas
        project.sale_order_ids.write({
            'x_studio_nv_numero_de_obra_relacionada': self.new_obra_nr
        })

        # Actualizar el campo en las transferencias (stock.picking) relacionadas
        project.stock_picking_ids.write({
            'x_studio_nv_numero_de_obra_relacionada': self.new_obra_nr
        })

        # Actualizar el campo en las transferencias (stock.picking) relacionadas
        project.lead_ids.write({
            'x_studio_nv_numero_de_obra_relacionada': self.new_obra_nr
        })

        
        return {'type': 'ir.actions.act_window_close'}
