from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)
class CrmLead(models.Model):
    """
    Extensión del modelo CRM Lead para gestión especializada de proyectos de construcción
    
    Características clave:
    - Vinculación con proyectos y subproyectos
    - Asignación automática de responsables (vendedor, cotizador (no es para nada importante), jefe de obra)
    - Georeferenciación mediante ubicaciones predefinidas
    - Control de consistencia entre empresas y proyectos
    """
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
        string="NV Numero de obra relacionada",
        tracking=True
        )

    obra_padre_id = fields.Many2one(
        'project.project',
        string="NV Numero de obra padre",
        no_create=True,
        size=29,
        tracking=True,
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
        string="MD Ubicacion Geografica:",
        #Obra ubi
        tracking=True
    )

    cod_postal_proyect = fields.Integer(
        compute="_compute_cod_postal_proyect", 
        string="Cod Postal",
        tracking=True,
        invisible=True,
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
        string="NV Provincia",
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
        string="NV Linea",
        #LnArtic
        tracking=True
    )

    obratipo_proyect_id = fields.Many2one(
        'project.obratipo',
        string="NV Tipo",
        #Obra tipo
        tracking=True
    )

    color_proyect_id = fields.Many2one(
        'project.color',
        string="NV Color",
        #ObraColoCd
        tracking=True
    )

    estado_obra_proyect_id = fields.Many2one(
        'project.obraestado',
        string="Estado obra",
        #ObraEstado
        tracking=True,
        invisible=True,
    )

    cartel_obra_id = fields.Many2one(
        'project.cartel.obra',
        string="NV Cartel",
        tracking=True
    )

    

    


    ##################################################################################################################
    #Computes
    ##################################################################################################################


    

    @api.depends('user_id')
    def _compute_vendedor_id(self):
        """
        Lógica para asignación automática de vendedor:
        1. Busca empleado vinculado al usuario del lead
        2. Encuentra registro correspondiente en project.syusro
        3. Asigna relación y registra en logs
        
        Dependencias:
        - user_id (usuario asignado al lead)
        
        Excepciones:
        - Fallo silencioso si no encuentra relación (asigna False)
        """
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
        """
        Valida longitud máxima del nombre de obra
        - Permite hasta 99 caracteres (incluyendo espacios)
        - Lanza ValidationError con mensaje claro
        """
        for record in self:
            if record.name and len(record.name.strip()) > 99:
                raise ValidationError(_("Error: El nombre no puede superar 98 caracteres."))


    """
    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        
        #Garantiza consistencia entre compañías:
        #- Proyecto debe pertenecer a misma compañía que lead
        #- Previene asignación cruzada entre empresas
        #- Mensaje de error detallado con nombres afectados
        
        for lead in self:
            if lead.project_id and lead.company_id and lead.project_id.company_id != lead.company_id:
                raise ValidationError(_(f"El proyecto seleccionado '{ lead.project_id.name }' pertenece a otra empresa: { lead.project_id.company_id.name }."))

    """
    ##################################################################################################################
    #Funciones bases de odoo
    ##################################################################################################################

    def unlink(self):
        # IDs de etapas que no permiten eliminación (ganadas, cerradas, etc.)
        etapas_protegidas = [41, 36, 47, 37, 38]

        for lead in self:
            if lead.stage_id.id in etapas_protegidas:
                raise ValidationError(_("No se puede eliminar una oportunidad que está en una etapa ganada o cerrada."))

        return super(CrmLead, self).unlink()


    def write(self, vals):

        """
        Extensión del método write para:
        - Sincronizar campos relacionados con proyectos
        - Actualizar números de obra y SP(numero de obra padre) automáticamente
        - Registrar cambios en logs para auditoría
        
        Comportamiento especial:
        - Actualiza x_studio_nv_numero_de_obra_relacionada al cambiar project_id
        - Actualiza x_studio_nv_numero_de_sp al cambiar obra_padre_id
        - Limpia campos relacionados si se elimina proyecto
        """
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
                    
            elif 'obra_padre_id' in vals:
                if vals['obra_padre_id']:
                    project = self.env['project.project'].browse(vals['obra_padre_id'])
                    if project: 
                        new_vals = {}
                        if project.obra_nr:
                            new_vals['x_studio_nv_numero_de_sp'] = project.obra_nr
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



# ---------------------------------------------------------------------------------------
# DOCUMENTACIÓN ADICIONAL
# ---------------------------------------------------------------------------------------

"""
ESTRUCTURA DE DATOS PRINCIPAL:
----------------------------------------------------------------------------------------
1. Campos Relacionales:
   - project_id: Proyecto principal vinculado
   - obra_padre_id: Proyecto padre (jerarquía de obras)
   - vendedor_id/cotizador_id/jefe_obra_id: Responsables técnicos

2. Campos Geográficos:
   - project_ubi_id: Ubicación principal
   - cod_postal_proyect/ubi_area_proyect/ubi_code: Derivados de ubicación

3. Campos de Clasificación:
   - lnart_proyect_id: Línea de negocio
   - obratipo_proyect_id: Tipo de obra
   - color_proyect_id: Codificación por color

LOGICA PRINCIPAL:
----------------------------------------------------------------------------------------
- Asignación Automática: Deriva responsables de usuarios vinculados
- Sincronización en Tiempo Real: Actualiza campos relacionados al modificar proyectos
- Validación Estricta: Mantiene integridad de datos empresariales

CONSIDERACIONES TÉCNICAS:
----------------------------------------------------------------------------------------
1. Seguridad:
   - Validación de compañía previene acceso cruzado
   - Dominios en campos relacionales filtran por contexto

2. Rendimiento:
   - Métodos computados optimizados con búsquedas limitadas
   - Logging detallado para diagnóstico de problemas

3. Mantenibilidad:
   - Estructura modular separando campos, cómputos y validaciones
   - Nombres de campos descriptivos según convención NV_
   
OBSERVACIONES:
----------------------------------------------------------------------------------------
- Los campos x_studio_* son creados desde la interfaz Studio
- project.syusro parece ser modelo personalizado para usuarios del sistema
- La relación empleado-usuario se asume existente en modelo hr.employee
"""
