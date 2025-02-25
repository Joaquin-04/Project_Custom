from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
    )
    
    def write(self, vals):
        _logger.warning("Write!!!")
        _logger.warning(f"valores: {vals}")
        
        if 'project_id' in vals:
            if vals['project_id']:
                
                # Se ha asignado un proyecto, obtenemos su información
                project = self.env['project.project'].browse(vals['project_id'])
                if project:
                    new_vals = {}
                    if project.obra_nr:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = project.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_obra_relacionada'] = False
                    if project.obra_padre_id:
                        new_vals['x_studio_nv_numero_de_obra_padre'] = project.obra_padre_id.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_obra_padre'] = False
                    vals.update(new_vals)
            else:
                # Se está borrando el proyecto, establecemos los campos en 0 o False
                vals.update({
                    'x_studio_nv_numero_de_obra_relacionada': 0,
                    'x_studio_nv_numero_de_obra_padre': 0,
                })
        return super(SaleOrder, self).write(vals)


    """
    def write(self, vals):
        _logger.warning("Write!!!")
        _logger.warning(f"valores: {vals}")

        if 'project_id' in vals:
            # Actualiza la cuenta analítica en las líneas de venta
            analytic_account = self.project_id.analytic_account_id
            _logger.warning(f"analytic_account: {analytic_account}")
            #for line in self.order_line:
            #    line.analytic_distribution = analytic_account

            # Actualiza los campos de Odoo Studio
            if self.project_id.obra_nr:
                _logger.warning(f" obra_nr {self.project_id.obra_nr}")
                self.x_studio_nv_numero_de_obra_relacionada = self.project_id.obra_nr
            if self.project_id.obra_padre_id:
                self.x_studio_nv_numero_de_obra_padre = self.project_id.obra_padre_id.obra_nr
            else:
                self.x_studio_nv_numero_de_obra_padre = False
        else:
            # Si se limpia el proyecto, se limpian también los campos
            self.x_studio_nv_numero_de_obra_relacionada = False
            self.x_studio_nv_numero_de_obra_padre = False
            

        return super(SaleOrder, self).write(vals)"""



    @api.onchange('project_id')
    def _onchange_project_id(self):
        _logger.warning("_onchange_project_id")
        if self.project_id:
            # Actualiza la cuenta analítica en las líneas de venta
            analytic_account = self.project_id.analytic_account_id
            _logger.warning(f"analytic_account: {analytic_account}")
            for line in self.order_line:
                line.analytic_distribution = analytic_account

            # Actualiza los campos de Odoo Studio
            if self.project_id.obra_nr:
                _logger.warning(f" obra_nr {self.project_id.obra_nr}")
                self.x_studio_nv_numero_de_obra_relacionada = self.project_id.obra_nr
            if self.project_id.obra_padre_id:
                self.x_studio_nv_numero_de_obra_padre = self.project_id.obra_padre_id.obra_nr
            else:
                self.x_studio_nv_numero_de_obra_padre = False
        else:
            # Si se limpia el proyecto, se limpian también los campos
            self.x_studio_nv_numero_de_obra_relacionada = False
            self.x_studio_nv_numero_de_obra_padre = False


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        """ Evita seleccionar un proyecto de otra empresa """
        for order in self:
            if order.project_id and order.company_id and order.project_id.company_id != order.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ order.project_id.name }' pertenece a otra empresa: { order.project_id.company_id.name }."))


    
    def action_confirm(self):
        """ Antes de confirmar la venta, abre un wizard para seleccionar o crear un proyecto """
        if not self.project_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order.project.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_sale_order_id': self.id,
                    'default_sale_company_id':self.company_id
                },
            }
        return super().action_confirm()





