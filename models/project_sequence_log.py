# project_sequence_log.py
from odoo import models, fields

class ProjectSequenceLog(models.Model):
    _name = 'project.sequence.log'
    _description = 'Log de asignación de secuencia para proyectos'
    _order = 'create_date desc'

    project_id = fields.Many2one(
        'project.project', 
        string="Proyecto", 
        ondelete="cascade",
        help="Proyecto al que se le asignó el número (si se creó)."
    )
    sequence_number = fields.Char(
        string="Número de Obra Asignado",
        required=True,
        help="Número asignado por la secuencia."
    )
    user_id = fields.Many2one(
        'res.users', 
        string="Usuario",
        default=lambda self: self.env.uid,
        help="Usuario que solicitó la asignación."
    )
    company_id = fields.Many2one(
        'res.company', 
        string="Compañía", 
        required=True,
        help="Compañía del proyecto."
    )
    message = fields.Text(
        string="Detalle",
        help="Información adicional sobre la asignación o error."
    )
    state = fields.Selection([
        ('success', 'Éxito'),
        ('error', 'Error'),
        ('warning', 'Advertencia'),
        ('other', 'Otro')
    ], default='other', string="Estado")
