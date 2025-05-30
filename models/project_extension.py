from odoo import models, fields, api, _
from odoo.exceptions import ValidationError,UserError
from psycopg2 import IntegrityError
import re

import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    """
    Extensión del modelo Project para gestión especializada de obras
    
    Funcionalidades Clave:
    - Numeración automática con secuencia configurable
    - Campos técnicos para integración con otros módulos
    - Sistema de estados y fechas clave
    - Gestión de relaciones padre-hijo entre proyectos
    - Auditoría detallada de creación/modificación
    """
    _inherit = ['project.project']  # Correcto

    # Relaciones inversas

    sale_order_ids = fields.One2many(
        'sale.order',
        'project_id',
        string="Órdenes de Venta",
        store=True,
        readonly=True,
        tracking=True
    )

    
    lead_ids = fields.One2many(
        'crm.lead',
        'project_id',
        string="Leads",
        readonly=True,
        tracking=True
    )

    
    stock_picking_ids = fields.One2many(
        'stock.picking',
        'project_id',
        string="Transferencias",
        readonly=True,
        tracking=True
    )


    # Campo 'name' sobreescrito con límite
    name = fields.Char(
        string="Nombre de la Obra",
        size=99,
        help="Nombre de la obra. Máximo 98 caracteres.",
        tracking=True
    )              

    obra_nr = fields.Char(
        string="Número de Obra",
        #readonly=True,
        #copy=False,
        readonly=True,
        copy=False,
        store=True,
        size=5,
        tracking=True
    )

    # Nuevo campo que sirve para la importación del excel
    obra_padre_nr = fields.Char(
        string = "Número de Obra Padre",
        readonly=False,
        copy=False,
        store=True,
        size=5,
        compute = "_compute_obra_padre_nr"
    )
    
    obra_padre_id = fields.Many2one(
        'project.project',
        string="Obra Padre",
        no_create=True,
        size=29,
        tracking=True,
        groups="Project_Custom.group_change_father_project"
    )

    color_proyect = fields.Many2one(
        'project.color',
        string="Color proyecto",
        #ObraColoCd
        tracking=True
    )

    estado_obra_proyect = fields.Many2one(
        'project.obraestado',
        string="Estado obra",
        #ObraEstado
        tracking=True
    )

    obra_estd_fc_ulti_modi = fields.Date(
        string="Última Modif. Estado de Obra",
        #readonly=True,
        readonly=True,
        help="Fecha en que se modificó por última vez el estado de la obra.",
        tracking=True
    )

    # CRM (x_studio_nv_linea)
    lnart_proyect = fields.Many2one(
        'project.lnarti',
        string="Ln Artic",
        #LnArtic
        tracking=True
    )

    obratipo_proyect = fields.Many2one(
        'project.obratipo',
        string="Obra Tipo",
        #Obra tipo
        tracking=True
    )

    obratipo_ubi = fields.Many2one(
        'project.ubic',
        string="Obra Ubicacion",
        #Obra ubi
        tracking=True
    )


    obra_ubi_nombre= fields.Char(
        #compute="_compute_obra_ubi_nombre,"
        compute="_compute_obra_ubi_nombre",
        Sring="Nombre",
        tracking=True
    )

    cod_postal_proyect = fields.Integer(
        #compute="_compute_cod_postal_proyect,"
        compute="_compute_cod_postal_proyect", 
        string="Cod Postal",
        tracking=True
    )

    ubi_area_proyect = fields.Integer(
        #compute="_compute_ubi_area_proyect,"
        compute="_compute_ubi_area_proyect", 
        string="Ubi Area",
        tracking=True
    )

    ubi_code = fields.Integer(
        #compute="_compute_ubi_code",
        compute="_compute_ubi_code",
        string="Código de ubicación",
        tracking=True
    )

    nombre_carga_obra = fields.Char(
        string="Nombre de carga Obra:",
        size=29,  # Original: 30 → 29
        tracking=True,
        invisible=True,
    )

    direccion = fields.Char(
        string="Dirección",
        size=79,  # Original: 80 → 79
        tracking=True
    )

    # --------------------------------------------------------------------------
    # NUEVOS CAMPOS (Basados en las columnas que NO están marcadas como 'ya')
    # --------------------------------------------------------------------------

    # 1. Fecha de Aprobación de Presupuesto (ej. ObraFcAlta)
    fecha_aprobacion_presupuesto = fields.Date(
        string="Fecha Aprob. Presupuesto",
        #compute="_compute_fecha_aprobacion_presupuesto",
        compute="_compute_fecha_aprobacion_presupuesto",
        store=True,
        help="Fecha de aprobación de presupuesto (solo fecha, sin hora)",
        tracking=True
    )

    # 2. Teléfonos y Fax (ObraTel1, ObraTel2, ObraFax1, ObraFax2)
    celular_1 = fields.Char(
        string="Celular 1",
        size=24,  # Original: 25 → 24
        tracking=True
    )

    telefono_fijo = fields.Char(
        string="Teléfono Fijo",
        size=24,  # Original: 25 → 24
        tracking=True
    )

    fax_1 = fields.Char(
        string="Fax 1",
        size=24,  # Original: 25 → 24
        tracking=True
    )

    fax_2 = fields.Char(
        string="Fax 2",
        size=24,  # Original: 25 → 24
        tracking=True
    )

    # 3. Tiempo proyectado (campo de ejemplo para “[[[[[tiempo proyectado]]]]]”)
    tiempo_proyectado = fields.Integer(
        string="Tiempo Proyectado",
        tracking=True
    )

    # 4. Observaciones (ObraObs)
    observaciones = fields.Text(
        string="Observaciones",
        tracking=True
    )

    # 5. Código Plus (ObraCdPlus)
    codigo_plus = fields.Char(
        string="Código Plus",
        size=59,  # Original: 60 → 59
        tracking=True
    )

    # 6. Fecha Probable de Entrega (ObraFcEntrPact / ObraFcEntrRene)
    fecha_pactada_entrega = fields.Date(
        string="Fecha Pactada de Entrega",
        tracking=True
    )
    fecha_renegociada_entrega = fields.Date(
        string="Fecha Renegociada de Entrega",
        tracking=True
    )

    # 7. Vendedor / Jefe / Técnico / Capataz (ObraVendCd, ObraJefeCd, ObraTecCd, ObraCapaCd)
    obra_vend_cd = fields.Many2one(
        'project.syusro', 
        string="Vendedor", 
        help="Código de Vendedor",
        tracking=True
    )
    obra_jefe_cd = fields.Many2one(
        'project.syusro', 
        string="Jefe", 
        help="Código de Jefe de Obra",
        tracking=True
    )
    obra_tec_cd = fields.Many2one(
        'project.syusro', 
        string="Técnico", 
        help="Código de Técnico",
        tracking=True
    )
    obra_capa_cd = fields.Many2one(
        'project.syusro', 
        string="Capataz", 
        help="Código de Capataz",
        tracking=True
    )

    # 8. Cartel Obra (ObraCartEstd) CRM (x_studio_nv_cartel)
    cartel_obra_id = fields.Many2one(
        'project.cartel.obra',
        string="Cartel de Obra",
        tracking=True
    )

    # 9. Indica si tiene Colocación (ObraColoca) -> asumiendo S/N
    tiene_colocacion = fields.Selection(
        [
            ('si', 'S'),
            ('no', 'N'),
        ],
        string="¿Tiene Colocación?",
        tracking=True
    )

    # 10. Empresa Origen (ObraEmprCd) - CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
    empresa_origen_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_empresa_origen_cd",
        compute="_compute_empresa_origen_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=1 NOA=2 GALVANIZADOS=3",
        tracking=True
    )

    obra_ref_fisc_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_obra_ref_fisc_cd",
        compute="_compute_obra_ref_fisc_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=4503 NOA=12873 GALVANIZADOS=13225",
        tracking=True
    )

    obra_ref_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_obra_ref_cd",
        compute="_compute_obra_ref_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=4503 NOA=12873 GALVANIZADOS=13225",
        tracking=True
    )

   
    # 11. Campo Adicional de Observaciones si se requiere
    #     (Si hubiera otra columna de Observaciones extra, se define aquí)
    extra_observaciones = fields.Text(
        string="Observaciones Extra",
        tracking=True
    )
    
    # 12. Campos de país y provincia si los tuvieras (PrvnCd, PaisCd) -> Asumimos guardarlos como Enteros
    # Reemplazar los campos prvn_cd y pais_cd por:
    provincia_id = fields.Many2one(
        'project.provincia',
        string="Provincia",
        help="Selecciona la provincia a la que pertenece el proyecto.",
        tracking=True
    )
    
    pais_cd = fields.Char(
        string="Código de País",
        #related="provincia_id.pais_cd",
        #readonly=True,
        related="provincia_id.pais_cd",
        readonly=True,
        store=True,
        help="Código de país obtenido de la provincia.",
        tracking=True
    )

    # 13 Kilogramos de Perfileria CRM(x_studio_nv_kg_perfilera)
    kg_perfileria = fields.Float(
        string="Kg de Perfileria",
        tracking=True
    )
    
    obra_cmpl = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0",
        invisible=True,
    )
    
    obra_ind_cmpl = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0",
        invisible=True,
    )
    
    obra_obs = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0",
        invisible=True,
    )
    
    obra_crc = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0",
        invisible=True,
    )



    




    # --------------------------------------------------------------------------
    # RESTRICCIONES Y COMPUTES
    # --------------------------------------------------------------------------
    
    @api.depends('obra_padre_id')
    def _compute_obra_padre_nr (self):
        for project in self:
            # El numero de la obra padre sera igual al numero de obra
            project['obra_padre_nr'] = project.obra_nr

            # Si el proyecto tiene obra padre entonces toma el numero de obra de la obra padre
            if project.obra_padre_id:
                project['obra_padre_nr'] = project.obra_padre_id.obra_nr

    

    
    
    @api.depends('company_id')
    def _compute_obra_ref_fisc_cd(self):
        for project in self:
            if project.company_id:
                # Toma el id de la empresa por defecto
                project.obra_ref_fisc_cd = project.company_id.id 
                
                # CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
                if project.company_id.id == 3:
                    # Cristalizando 
                    project.obra_ref_fisc_cd = 4503
                elif project.company_id.id == 2:
                    # Noa Aberturas
                    project.obra_ref_fisc_cd = 12873
                elif project.company_id.id == 4:
                    # Galvanizados del Norte
                    project.obra_ref_fisc_cd = 13225
                
            else:
                project.obra_ref_fisc_cd = False

    
    
    @api.depends('company_id')
    def _compute_obra_ref_cd(self):
        for project in self:
            if project.company_id:
                # Toma el id de la empresa por defecto
                project.obra_ref_cd = project.company_id.id 
                
                # CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
                if project.company_id.id == 3:
                    # Cristalizando 
                    project.obra_ref_cd = 4503
                elif project.company_id.id == 2:
                    # Noa Aberturas
                    project.obra_ref_cd = 12873
                elif project.company_id.id == 4:
                    # Galvanizados del Norte
                    project.obra_ref_cd = 13225
                
            else:
                project.obra_ref_cd = False
        
                


    @api.depends('company_id')
    def _compute_empresa_origen_cd(self):
        for project in self:
            if project.company_id:
                # Toma el id de la empresa por defecto
                project.empresa_origen_cd = project.company_id.id 
                
                # CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
                if project.company_id.id == 3:
                    # Cristalizando 
                    project.empresa_origen_cd = 1
                elif project.company_id.id == 2:
                    # Noa Aberturas
                    project.empresa_origen_cd = 2
                elif project.company_id.id == 4:
                    # Galvanizados del Norte
                    project.empresa_origen_cd = 3

            else:
                project.empresa_origen_cd = False

    
    @api.depends('create_date')
    def _compute_fecha_aprobacion_presupuesto(self):
        for project in self:
            if project.create_date:
                # Convertimos el create_date (datetime) a date
                project.fecha_aprobacion_presupuesto = fields.Date.from_string(project.create_date)
                project.obra_estd_fc_ulti_modi = fields.Date.from_string(project.create_date)
            else:
                project.fecha_aprobacion_presupuesto = False
                project.obra_estd_fc_ulti_modi = False

    

    
    @api.depends('obratipo_ubi')
    def _compute_cod_postal_proyect(self):
        for record in self:
            if record.obratipo_ubi:
                # Asignamos el valor del código postal desde 'ubic_cp' de 'obratipo_ubi'
                record.cod_postal_proyect = record.obratipo_ubi.ubic_cp
            else:
                # Si no hay obra seleccionada, lo dejamos vacío o en 0
                record.cod_postal_proyect = 0

    

    @api.depends('obratipo_ubi')
    def _compute_obra_ubi_nombre(self):
        for record in self:
            record.obra_ubi_nombre = record.obratipo_ubi.ubic_nm if record.obratipo_ubi else ''

    

    @api.depends('obratipo_ubi')
    def _compute_ubi_area_proyect(self):
        for record in self:
            record.ubi_area_proyect = record.obratipo_ubi.ubic_area_cd if record.obratipo_ubi else ''

    
    @api.depends('obratipo_ubi')
    def _compute_ubi_code(self):
        for record in self:
            record.ubi_code = record.obratipo_ubi.ubic_cd if record.obratipo_ubi else ''
            

    def _compute_display_name(self):
        for record in self:
            if record.obra_nr:
                record.display_name = f"[{record.obra_nr}] {record.name}"
            else:
                record.display_name = record.name

    
    
    
    

    _sql_constraints = [
        ('obra_nr_unique', 'UNIQUE(obra_nr)', '¡El número de obra debe ser único!'),
    ]


    @api.constrains('obra_nr')
    def _check_obra_nr_unique(self):
        for project in self:
            if project.obra_nr:
                existing = self.search([
                    ('obra_nr', '=', project.obra_nr),
                    ('id', '!=', project.id)
                ], limit=1)
                if existing:
                    raise ValidationError(f"¡El número de obra {project.obra_nr} ya existe!")
                    

    @api.constrains('cod_postal_proyect')
    def _check_cod_postal_proyect(self):
        for record in self:
            if record.cod_postal_proyect and len(str(record.cod_postal_proyect)) > 14:  # Original: 15 (alnum) → 14 dígitos
                raise ValidationError(_("Código postal no puede exceder 14 dígitos."))

    @api.constrains('ubi_area_proyect')
    def _check_ubi_area_proyect(self):
        for record in self:
            if record.ubi_area_proyect and len(str(record.ubi_area_proyect)) > 5:  # Original: 5 (alnum) → 4 dígitos
                raise ValidationError(_("Ubicación área no puede exceder 5 dígitos."))

    @api.constrains('observaciones')
    def _check_observaciones_length(self):
        for record in self:
            if record.observaciones and len(record.observaciones) > 199:  # Original: 200 → 199
                raise ValidationError(_("Observaciones no puede exceder 199 caracteres."))

    @api.constrains('extra_observaciones')
    def _check_extra_observaciones_length(self):
        for record in self:
            if record.extra_observaciones and len(record.extra_observaciones) > 199:  # Asumiendo misma lógica
                raise ValidationError(_("Observaciones extra no puede exceder 199 caracteres."))

    


    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name.strip()) > 99:
                raise ValidationError(_("Error: El nombre no puede superar 98 caracteres."))


    @api.constrains('kg_perfileria')
    def _check_kg_perfileria(self):
        for record in self:
            if record.kg_perfileria > 99999:  # Original: 6 dígitos → 5 (99999)
                raise ValidationError(_("Kg de perfilería no puede exceder 99999."))
    # --------------------------------------------------------------------------
    # ONCHANGE'S
    # --------------------------------------------------------------------------
    
    # Lista de campos que NO deben heredar valores (obra_nr y obra_padre_id)
    
    
    
    
    # 2. Campos que SIEMPRE se heredarán (aunque sean computados/relacionados)
    FIELDS_TO_INCLUDE = [
        'obratipo_ubi',
        'cod_postal_proyect',
        'ubi_area_proyect',
        'direccion',
        'codigo_plus',
        'provincia_id',
        'pais_cd',
    ]
    """Hereda automáticamente los valores del proyecto padre al seleccionarlo."""
    
    @api.onchange('obra_padre_id')
    def _onchange_obra_padre_id(self):
        if self.obra_padre_id:
            padre = self.obra_padre_id
            for field_name in self._fields:
                if (
                    field_name in self.FIELDS_TO_INCLUDE 
                    and (
                        not self._fields[field_name].compute 
                        and not self._fields[field_name].related
                    )
                ):
                    valor = padre[field_name]
                    # Validación para el campo tiene_colocacion
                    if field_name == 'tiene_colocacion':
                        if valor == 'S':
                            valor = 'si'
                        elif valor == 'N':
                            valor = 'no'

                    if not self[field_name] :
                        self[field_name] = valor


    # --------------------------------------------------------------------------
    # FUNCIONES BASE DE ODOO
    # --------------------------------------------------------------------------

    """
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):

        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
        
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('obra_nr', operator, name), ('name', operator, name)] + domain
            
        #_logger.warning(f"*****************************  _name_search ****************************")
        #_logger.warning(f"name: {name} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        rtn = self._search(domain, limit=limit, order=order)
        #_logger.warning(f"rtn: {rtn}")
        return rtn

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        if domain is None:  
            domain = []  # Si domain es None, lo inicializamos como una lista vacía
    
        if name:
            # Agregar condiciones de búsqueda (obra_nr o name)
            domain = ['|', ('obra_nr', operator, name), ('name', operator, name)] + domain
    
        # **Forzar la búsqueda sin restricciones de compañía**
        domain = [('company_id', 'in', self.env['res.company'].search([]).ids)] + domain
    
        # Registrar en logs para depuración
        _logger.warning(f"*****************************  _name_search ****************************")
        _logger.warning(f"name: {name} \ndomain {domain} \noperator: {operator} \nlimit: {limit} \norder: {order} \nname_get_uid: {name_get_uid}")
        
        # Realizar la búsqueda con el dominio actualizado
        rtn = self.with_context(allowed_company_ids=self.env['res.company'].search([]).ids)._search(domain, limit=limit, order=order)
        
        _logger.warning(f"rtn: {rtn}")
        return rtn
    """

    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        if domain is None:  
            domain = []
        
        if name:
            domain = ['|', ('obra_nr', operator, name), ('name', operator, name)] + domain
        
        # ELIMINAR CUALQUIER FILTRO RELACIONADO CON EMPRESAS
        # 1. Quitar cualquier condición existente sobre company_id
        domain = [d for d in domain if d[0] != 'company_id']
        
        # 2. Buscar sin restricciones de empresa
        return self._search(domain, limit=limit, order=order)


        

    

    

    @api.model
    def create(self, vals):
        """
        Sobreescritura del método create para:
        1. Limpiar formatos de teléfono
        2. Asignar compañía por defecto
        3. Crear cuenta analítica asociada
        4. Generar número de obra secuencial
        5. Registrar auditoría detallada
        
        Flujo de Excepciones:
        - ValidationError: Errores de validación de datos
        - IntegrityError: Conflictos de base de datos
        - Exception: Errores generales
        
        Registra en:
        - project.sequence.log: Auditoría de numeración
        """
        # Definir una función para limpiar los números de teléfono
        def limpiar_numero_telefono(numero):
            if numero:
                # Eliminar todos los caracteres no numéricos incluyendo '+' y espacios
                numero_limpio = re.sub(r'[^\d]', '', numero)
                # Eliminar ceros iniciales si es necesario (opcional)
                return numero_limpio.lstrip('0') if numero_limpio else None
            return numero

        # Limpiar los campos de números de teléfono
        campos_telefono = ['celular_1', 'telefono_fijo', 'fax_1', 'fax_2']
        for campo in campos_telefono:
            if campo in vals:
                vals[campo] = limpiar_numero_telefono(vals[campo])


        if 'kg_perfileria' in vals:
            vals['kg_perfileria']=round(vals['kg_perfileria'])


        
        # Asignar la compañía si no se proporcionó
        if not vals.get('company_id'):
            vals['company_id'] = self.env.company.id

        
        # Crear cuenta analítica automáticamente
        if not vals.get('analytic_account_id'):
            analytic_account = self.env['account.analytic.account'].create({
                'name': vals.get('name'),
                'company_id': vals['company_id'],
                'plan_id': 1,
            })
            vals['analytic_account_id'] = analytic_account.id

        
        #Por defecto poner el estado de la obra en 2001
        estado_de_iniciio = self.env['project.obraestado'].search([('cod','=','2001')],limit=1)
        if estado_de_iniciio:
            vals['estado_obra_proyect'] = estado_de_iniciio.id

        

        try:
            # Intentar crear el proyecto
            record = super(ProjectProject, self).create(vals)

            # Generar número de obra secuencial y asignarlo al proyecto
            next_value = self.env['ir.sequence'].next_by_code('custom.project.number')
            record.write({'obra_nr': next_value})

            # Registrar el log de auditoría para creación exitosa
            audit_vals = {
                'project_id': record.id,
                'sequence_number': next_value,
                'user_id': self.env.uid,
                'company_id': record.company_id.id,
                'state': 'success',
                'message': 'Proyecto creado y secuencia asignada exitosamente.'
            }
            self.env['project.sequence.log'].sudo().create(audit_vals)

            
            return record

        except ValidationError as ve:
            # Registrar el log de auditoría para errores de validación
            audit_vals = {
                'project_id': False,
                'sequence_number': None,
                'user_id': self.env.uid,
                'company_id': vals.get('company_id'),
                'state': 'error',
                'message': f'Error de validación al crear el proyecto: {str(ve)}',
                'data': vals
            }
            self.env['project.sequence.log'].sudo().create(audit_vals)
            _logger.error(f"Error de validación al crear el proyecto: {str(ve)}")
            raise ve

        except IntegrityError as ie:
            # Registrar el log de auditoría para errores de integridad
            audit_vals = {
                'project_id': False,
                'sequence_number': None,
                'user_id': self.env.uid,
                'company_id': vals.get('company_id'),
                'state': 'error',
                'message': f'Error de integridad al crear el proyecto: {str(ie)}',
                'data': vals
            }
            self.env['project.sequence.log'].sudo().create(audit_vals)
            _logger.error(f"Error de integridad al crear el proyecto: {str(ie)}")
            raise ValidationError(_('Ocurrió un error de integridad al crear el proyecto. Por favor, inténtelo de nuevo.'))

        except Exception as e:
            # Registrar el log de auditoría para errores generales
            audit_vals = {
                'project_id': False,
                'sequence_number': None,
                'user_id': self.env.uid,
                'company_id': vals.get('company_id'),
                'state': 'error',
                'message': f'Error general al crear el proyecto: {str(e)}',
                'data': vals
            }
            self.env['project.sequence.log'].sudo().create(audit_vals)
            _logger.error(f"Error general al crear el proyecto: {str(e)}")
            raise ValidationError(_('Ocurrió un error al crear el proyecto. Por favor, inténtelo de nuevo.'))


    def write(self, vals):
        """
        Actualización de proyectos:
        - Actualiza fecha de modificación de estado automáticamente
        - Propaga cambios a registros relacionados
        """
        # Si se está cambiando el estado de obra, se actualiza la fecha a la fecha actual.
        if 'estado_obra_proyect' in vals:
            vals['obra_estd_fc_ulti_modi'] = fields.Date.context_today(self)

        # Definir campos y sus propagaciones específicas por modelo
        """
        propagation_map = {
            # Campo: {Modelo: campo_destino}
            'obra_padre_id': {
                'crm.lead': 'project_id',
                'sale.order': 'project_id',
                'stock.picking': 'project_id',
            },
            'name': {
                'crm.lead': 'x_studio_nv_nombre_de_la_obra',
                'sale.order': 'x_studio_nv_nombre_de_la_obra',
            },
            'direccion': {
                'crm.lead': 'x_studio_nv_direccin',
            },
            'lnart_proyect': {
                'crm.lead': 'x_studio_nv_linea',
                'sale.order': 'x_studio_nv_linea',
            },
            'kg_perfileria': {
                'crm.lead': 'x_studio_nv_kg_perfilera',
                'sale.order': 'x_studio_nv_kg_perfilera',
            },
            # Agregar más campos según sea necesario
        }
        """
        propagation_map = {
            # Campo: {Modelo: campo_destino}
            'obra_padre_id': {
                'crm.lead': 'obra_padre_id', # project.project
                'sale.order': 'x_studio_nv_numero_de_obra_padre', # entero que tiene que tomar el valor de obra_padre_nr del proyecto
                'stock.picking': 'x_studio_nv_numero_de_obra_padre', # entero que tiene que tomar el valor de obra_padre_nr del proyecto
            },
        }

        # Preparar cambios para cada modelo
        changes = {
            'crm.lead': {},
            'sale.order': {},
            'stock.picking': {},
        }
        # Identificar campos modificados que necesitan propagación
        for field, model_map in propagation_map.items():
            if field in vals:
                for model_name, dest_field in model_map.items():
                    if dest_field:
                        changes[model_name][dest_field] = vals[field]

        # Ejecutar escritura normal
        res = super(ProjectProject, self).write(vals)
        
        # Manejo especial para la propagación de obra_padre_id
        if 'obra_padre_id' in vals:
            for project in self:
                # Obtener el valor real de obra_padre_nr después de la escritura
                nr_obra = project.obra_nr
                parent_nr = project.obra_padre_nr 
                
                # Actualizar leads (campo Many2one)
                if project.lead_ids:
                    # Para leads, usamos el ID del proyecto padre
                    
                    padre = self.env['project.project'].search([('obra_nr','=',parent_nr)])
                    project.lead_ids.write({
                        'obra_padre_id': padre
                    })
                
                # Actualizar órdenes de venta (campo char)
                if project.sale_order_ids:
                    # Para ventas, usamos el número de obra del padre
                    project.sale_order_ids.write({
                        'x_studio_nv_numero_de_obra_relacionada':nr_obra,
                        'x_studio_nv_numero_de_obra_padre': parent_nr
                    })
                
                # Actualizar remitos (campo char)
                if project.stock_picking_ids:
                    # Para remitos, usamos el número de obra del padre
                    project.stock_picking_ids.write({
                        'x_studio_nv_numero_de_obra_relacionada':nr_obra,
                        'x_studio_nv_numero_de_obra_padre': parent_nr
                    })

        else:
            #raise UserError(f" cambios:  {changes} \n{seld}")
            # Propagación de cambios a registros relacionados
            for project in self:
                # Actualizar leads
                if project.lead_ids and changes['crm.lead']:
                    project.lead_ids.write(changes['crm.lead'])
                
                # Actualizar órdenes de venta
                if project.sale_order_ids and changes['sale.order']:
                    project.sale_order_ids.write(changes['sale.order'])
                
                # Actualizar remitos (solo campos específicos)
                if project.stock_picking_ids and changes['stock.picking']:
                    project.stock_picking_ids.write(changes['stock.picking'])

        
        

        
        return res



