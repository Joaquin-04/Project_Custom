from odoo import models, fields, api
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Campo 'name' sobreescrito con límite
    name = fields.Char(
        string="Nombre de la Obra",
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
        tracking=True
    )
    
    cotizador_id = fields.Many2one(
        'project.syusro', 
        string="NV cotizador", 
        help="Código del Cotizador",
        tracking=True
    )
    
    jefe_obra_id = fields.Many2one(
        'project.syusro', 
        string="NV Jefe de Obra", 
        help="Código de Jefe de Obra",
        tracking=True
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

    

    


    ##################################################################################################################
    #Computes
    ##################################################################################################################

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



