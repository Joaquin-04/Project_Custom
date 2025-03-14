from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campo 'name' sobreescrito con límite
    name = fields.Char(
        string="",
        size=99,
        help="Nombre de la obra. Máximo 98 caracteres.",
        tracking=True
    )
    
    project_id = fields.Many2one(
        'project.project',
        string="Proyecto",
        domain="[('company_id', '=', company_id)]",
        tracking=True
        )

    vendedor_id = fields.Many2one(
        'project.syusro', 
        string="Vendedor", 
        help="Código de Vendedor",
        tracking=True,
        compute="_compute_vendedor_id",
        store=True,
        readonly=False,
    )
    
    cotizador_id = fields.Many2one(
        'project.syusro', 
        string="NV cotizador", 
        help="Código del Cotizador",
        tracking=True,
        compute="_compute_cotizador_id",
        store=True,
        readonly=False,
    )
    
    jefe_obra_id = fields.Many2one(
        'project.syusro', 
        string="NV Jefe de Obra", 
        help="Código de Jefe de Obra",
        tracking=True,
        compute="_compute_jefe_obra_id",
        store=True,
        readonly=False,
    )

    project_ubi_id = fields.Many2one(
        'project.ubic',
        string="Obra Ubicacion",
        #Obra ubi
        tracking=True
    )

    cod_postal_proyect = fields.Integer(
        compute="_compute_cod_postal_proyect", 
        string="Cod Postal",
        tracking=True
    )

    ubi_area_proyect = fields.Integer(
        compute="_compute_ubi_area_proyect", 
        string="Ubi Area",
        tracking=True
    )

    ubi_code = fields.Integer(
        compute="_compute_ubi_code", 
        string="Código de ubicación",
        tracking=True
    )

    provincia_id = fields.Many2one(
        'project.provincia',
        string="Provincia",
        help="Selecciona la provincia a la que pertenece el proyecto.",
        tracking=True
    )
    
    pais_cd = fields.Char(
        string="Código de País",
        related="provincia_id.pais_cd",
        store=True,
        readonly=True,
        help="Código de país obtenido de la provincia.",
        tracking=True
    )

    lnart_proyect_id = fields.Many2one(
        'project.lnarti',
        string="Linea",
        #LnArtic
        tracking=True
    )

    obratipo_proyect_id = fields.Many2one(
        'project.obratipo',
        string="Obra Tipo",
        #Obra tipo
        tracking=True
    )

    color_proyect_id = fields.Many2one(
        'project.color',
        string="Color proyecto",
        #ObraColoCd
        tracking=True
    )

    estado_obra_proyect_id = fields.Many2one(
        'project.obraestado',
        string="Estado obra",
        #ObraEstado
        tracking=True
    )

    cartel_obra_id = fields.Many2one(
        'project.cartel.obra',
        string="Cartel de Obra",
        tracking=True
    )

    

    


    ##################################################################################################################
    #Computes
    ##################################################################################################################

    @api.depends('user_id')
    def _compute_vendedor_id(self):
        for lead in self:
            if lead.user_id:
                # Buscar al empleado cuyo user_id coincide con el user del lead
                employee = self.env['hr.employee'].search([('user_id', '=', lead.user_id.id)], limit=1)
                if employee:
                    _logger.warning(f"empleados: {employee}")
                    # Buscar en project.syusro aquel registro que tenga al empleado relacionado
                    syusro = self.env['project.syusro'].search([('employee_ids', 'in', employee.id)], limit=1)
                    _logger.warning(f"usuarios del sistema gx: {syusro}")
                    lead.vendedor_id = syusro.id
                    _logger.warning("Asignado vendedor %s para el lead %s", syusro.display_name, lead.name)
                else:
                    lead.vendedor_id = False
            else:
                lead.vendedor_id = False


    @api.depends('x_studio_nv_cotizador')
    def _compute_cotizador_id(self):
        for lead in self:
            if lead.x_studio_nv_cotizador:
                # Buscar al empleado cuyo user_id coincide con el user del lead
                employee = self.env['hr.employee'].search([('user_id', '=', lead.x_studio_nv_cotizador.id)], limit=1)
                if employee:
                    _logger.warning(f"empleados: {employee}")
                    # Buscar en project.syusro aquel registro que tenga al empleado relacionado
                    syusro = self.env['project.syusro'].search([('employee_ids', 'in', employee.id)], limit=1)
                    _logger.warning(f"usuarios del sistema gx: {syusro}")
                    lead.cotizador_id = syusro.id
                    _logger.warning("Asignado cotizador_id %s para el lead %s", syusro.display_name, lead.name)
                else:
                    lead.cotizador_id = False
            else:
                lead.cotizador_id = False


    @api.depends('x_studio_many2one_field_EvMqQ')
    def _compute_jefe_obra_id(self):
        for lead in self:
            if lead.x_studio_many2one_field_EvMqQ:
                # Buscar al empleado cuyo user_id coincide con el user del lead
                employee = self.env['hr.employee'].search([('user_id', '=', lead.x_studio_many2one_field_EvMqQ.id)], limit=1)
                if employee:
                    _logger.warning(f"empleados: {employee}")
                    # Buscar en project.syusro aquel registro que tenga al empleado relacionado
                    syusro = self.env['project.syusro'].search([('employee_ids', 'in', employee.id)], limit=1)
                    _logger.warning(f"usuarios del sistema gx: {syusro}")
                    lead.jefe_obra_id = syusro.id
                    _logger.warning("Asignado jefe_obra_id %s para el lead %s", syusro.display_name, lead.name)
                else:
                    lead.jefe_obra_id = False
            else:
                lead.jefe_obra_id = False


    
    
    @api.depends('project_ubi_id')
    def _compute_cod_postal_proyect(self):
        for record in self:
            if record.project_ubi_id:
                # Asignamos el valor del código postal desde 'ubic_cp' de 'project_ubi_id'
                record.cod_postal_proyect = record.project_ubi_id.ubic_cp
            else:
                # Si no hay obra seleccionada, lo dejamos vacío o en 0
                record.cod_postal_proyect = 0

    

    @api.depends('project_ubi_id')
    def _compute_ubi_area_proyect(self):
        for record in self:
            record.ubi_area_proyect = record.project_ubi_id.ubic_area_cd if record.project_ubi_id else ''


    @api.depends('project_ubi_id')
    def _compute_ubi_code(self):
        for record in self:
            record.ubi_code = record.project_ubi_id.ubic_cd if record.project_ubi_id else ''
   ##################################################################################################################
    #Restricciones
    ################################################################################################################## 

    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name.strip()) > 99:
                raise ValidationError(_("Error: El nombre no puede superar 98 caracteres."))


    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        """ Evita seleccionar un proyecto de otra empresa """
        for lead in self:
            if lead.project_id and lead.company_id and lead.project_id.company_id != lead.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ lead.project_id.name }' pertenece a otra empresa: { lead.project_id.company_id.name }."))

    ##################################################################################################################
    #Funciones bases de odoo
    ##################################################################################################################

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
                        new_vals['x_studio_nv_numero_de_sp'] = project.obra_padre_id.obra_nr
                    else:
                        new_vals['x_studio_nv_numero_de_sp'] = False
                    vals.update(new_vals)
            else:
                # Se está borrando el proyecto, establecemos los campos en 0 o False
                vals.update({
                    'x_studio_nv_numero_de_obra_relacionada': 0,
                    'x_studio_nv_numero_de_sp': 0,
                })
        return super(CrmLead, self).write(vals)



