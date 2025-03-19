from odoo import models, fields,api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', 'in', allowed_company_ids)]",
        #compute="_compute_project_id",
        readonly=False
    )

    def _compute_project_id(self):
        _logger.warning(f"**********************************************COMPUTE**********************************************")
        for picking in self:
            if picking.x_studio_nv_numero_de_obra_relacionada:
                obra_nr = picking.x_studio_nv_numero_de_obra_relacionada
                proyecto = self.env['project.project'].search([('obra_nr','=',obra_nr)])
                _logger.warning(f"Proyecto {proyecto.name} asignado al remito {picking.name}")
            else:
                _logger.warning(f"No se a asignado asignado nada al remito {picking.name}")
                picking.project_id = False


    #Me sirve para los casos de remito creados con la reserva de materiales
    @api.model
    def create(self, vals):
        # Llamamos al método create original para crear el registro
        picking = super(StockPicking, self).create(vals)

        _logger.warning(f"**********************************************CREATE PROYECTO**********************************************")
        obra_nr = picking.x_studio_nv_numero_de_obra_relacionada
        proyecto = self.env['project.project'].search([('obra_nr','=',obra_nr)])
        _logger.warning(f"OBRA: {obra_nr}\n PROYECTO: {proyecto} ")
        if proyecto: 
            # Asignamos el proyecto de la venta al remito
            picking.project_id = proyecto.id
            _logger.warning(f"Proyecto {proyecto.name} asignado al remito {picking.name}")

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



