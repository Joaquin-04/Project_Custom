from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrderProjectWizard(models.TransientModel):
    _name = 'sale.order.project.wizard'
    _description = 'Seleccionar o Crear Proyecto'

    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", required=True)
    project_id = fields.Many2one(
        'project.project', 
        string="Proyecto Existente", 
        domain="[('company_id', '=', sale_order_id.company_id)]"
    )
    create_new = fields.Boolean(string="Crear Nuevo Proyecto")
    new_project_name = fields.Char(string="Nombre del Nuevo Proyecto")

    def action_apply(self):
        """ Asigna el proyecto seleccionado o crea uno nuevo """
        if self.create_new:
            if not self.new_project_name:
                raise UserError(_("Debe ingresar un nombre para el nuevo proyecto."))
            project = self.env['project.project'].create({
                'name': self.new_project_name,
                'company_id': self.sale_order_id.company_id.id,
            })
        else:
            project = self.project_id

        self.sale_order_id.project_id = project
        self.sale_order_id._onchange_project_id()
