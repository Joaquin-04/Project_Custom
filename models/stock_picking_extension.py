from odoo import models, fields,api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', 'in', allowed_company_ids)]"
    )

    @api.model
    def create(self, vals):
        # Llamamos al método create original para crear el registro
        picking = super(StockPicking, self).create(vals)

        # Buscamos la venta relacionada
        sale_order = picking.sale_id 
        if sale_order and sale_order.project_id:
            # Asignamos el proyecto de la venta al remito
            picking.project_id = sale_order.project_id
            _logger.info(f"Proyecto {sale_order.project_id.name} asignado al remito {picking.name}")
        
        sale_order = picking.sale_stock_link_id.sale_order_id
        if sale_order and sale_order.project_id:
            # Asignamos el proyecto de la venta al remito
            picking.project_id = sale_order.project_id
            _logger.info(f"Proyecto {sale_order.project_id.name} asignado al remito {picking.name}")
        

        return picking


    @api.onchange('sale_id')
    def _onchange_sale_id(self):
        _logger.warning("Write!!! Que se activa desde proyecto")
        _logger.warning(f"valores: {vals}")
        if self.sale_id and self.sale_id.project_id:
            self.project_id = self.sale_id.project_id
            analytic_account = self.sale_id.project_id.analytic_account_id
            for move in self.move_lines:
                move.analytic_account_id = analytic_account



    def write(self, vals):
        _logger.warning("Write!!! Que se activa desde proyecto")
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
        return super(StockPicking, self).write(vals)



