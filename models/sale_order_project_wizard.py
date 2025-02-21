from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrderProjectWizard(models.TransientModel):
    _name = 'sale.order.project.wizard'
    _description = 'Seleccionar o Crear Proyecto'

    sale_order_id = fields.Many2one('sale.order', string="Orden de Venta", required=True)

    company_id = fields.Many2one(
        'res.company', 
        string="Compañía",
        related='sale_order_id.company_id',
        readonly=True
    )
    
    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', '=', company_id)]"
    )

    
    create_new = fields.Boolean(string="Crear Nuevo Proyecto?")
    
    new_project_name = fields.Char(string="Nombre del Nuevo Proyecto")

    obra_padre_id = fields.Many2one(
        'project.project', 
        string="Obra Padre",
        domain="[('company_id', '=', company_id)]"
    )


    @api.model
    def default_get(self, fields_list):
        """Obtiene valores por defecto, como el nombre del lead si proviene de uno"""
        res = super(SaleOrderProjectWizard, self).default_get(fields_list)
        sale_order = self.env['sale.order'].browse(self.env.context.get('default_sale_order_id'))
        project_id = sale_order.project_id

        
        if project_id:
            res['project_id']=project_id
        
        if sale_order.opportunity_id:  # Si la orden proviene de un lead
            res['new_project_name'] = sale_order.opportunity_id.name

        return res

    @api.constrains('create_new', 'project_id')
    def _check_project_selection(self):
        """Valida que si no se crea un nuevo proyecto, el campo project_id no esté vacío"""
        for wizard in self:
            if not wizard.create_new and not wizard.project_id:
                raise ValidationError(_("Debe seleccionar un proyecto si no va a crear uno nuevo."))


    

    def action_apply(self):
        """ Aplica la selección del proyecto o crea uno nuevo con validaciones"""
        if self.create_new:
            if not self.new_project_name:
                raise UserError(_("Debe ingresar un nombre para el nuevo proyecto."))

            project = self.env['project.project'].create({
                'name': self.new_project_name,
                'company_id': self.sale_order_id.company_id.id,
                'obra_padre_id': self.obra_padre_id.id if self.obra_padre_id else False,
            })
        else:
            project = self.project_id

        # Asignar el proyecto a la orden de venta
        self.sale_order_id.project_id = project
        self.sale_order_id._onchange_project_id()

        #Confirmar la orden de venta
        self.sale_order_id.action_confirm()

        


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        for record in self:
            if record.project_id and record.company_id != record.project_id.company_id:
                raise ValidationError(_(
                    f"El proyecto seleccionado '{record.project_id.name}' pertenece a otra empresa: {record.project_id.company_id.name}."
                ))





