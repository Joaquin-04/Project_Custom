from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
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

    lead_ids = fields.Many2many(
        'crm.lead',
        'project_crm_rel',    # Nombre de la tabla relacional
        'project_id',         # Columna para el ID de project.project
        'crm_lead_id',        # Columna para el ID de crm.lead
        string="Leads",
        store=True,
        readonly=True,
        tracking=True
    )

    stock_picking_ids = fields.Many2many(
        'stock.picking',
        'project_stock_picking_rel',  # Nombre de la tabla relacional
        'project_id',                 # Columna para el ID de project.project
        'stock_picking_id',           # Columna para el ID de stock.picking
        string="Transferencias",
        store=True,
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
        store=True,
        size=5,
        tracking=True
    )
    
    obra_padre_id = fields.Many2one(
        'project.project',
        string="Obra Padre",
        domain="[('company_id', '=', company_id)]",  # Filtra por compañías permitidas
        no_create=True,
        size=29,
        tracking=True
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
        #compute="_compute_obra_ubi_nombre",
        Sring="Nombre",
        tracking=True
    )

    cod_postal_proyect = fields.Integer(
        #compute="_compute_cod_postal_proyect", 
        string="Cod Postal",
        tracking=True
    )

    ubi_area_proyect = fields.Integer(
        #compute="_compute_ubi_area_proyect", 
        string="Ubi Area",
        tracking=True
    )

    ubi_code = fields.Integer(
        #compute="_compute_ubi_code", 
        string="Código de ubicación",
        tracking=True
    )

    nombre_carga_obra = fields.Char(
        string="Nombre de carga Obra:",
        size=29,  # Original: 30 → 29
        tracking=True
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
            ('S', 'Sí'),
            ('N', 'No'),
        ],
        string="¿Tiene Colocación?",
        tracking=True
    )

    # 10. Empresa Origen (ObraEmprCd) - CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
    empresa_origen_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_empresa_origen_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=1 NOA=2 GALVANIZADOS=3",
        tracking=True
    )

    obra_ref_fisc_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_obra_ref_fisc_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=4503 NOA=12873 GALVANIZADOS=13225",
        tracking=True
    )

    obra_ref_cd = fields.Integer(
        string="Empresa Origen Código",
        #compute="_compute_obra_ref_cd",
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
        default="0"
    )
    
    obra_ind_cmpl = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0"
    )
    
    obra_obs = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0"
    )
    
    obra_crc = fields.Char(
        string="YA casi no se usa",
        tracking=True,
        default="0"
    )



    




    # --------------------------------------------------------------------------
    # RESTRICCIONES Y COMPUTES
    # --------------------------------------------------------------------------
    
    

    
    
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
            else:
                project.fecha_aprobacion_presupuesto = False

    

    
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

    
    
    
    

    """
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

                    
    """

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
        'color_proyect',
        'estado_obra_proyect',
        'obra_estd_fc_ulti_modi',
        'lnart_proyect',
        'obratipo_proyect',
        'obratipo_ubi',
        'cod_postal_proyect',
        'ubi_area_proyect',
        'nombre_carga_obra',
        'direccion',
        'celular_1',
        'telefono_fijo',
        'fax_1',
        'fax_2',
        'tiempo_proyectado',
        'observaciones',
        'codigo_plus',
        'fecha_pactada_entrega',
        'fecha_renegociada_entrega',
        'obra_vend_cd',
        'obra_jefe_cd',
        'obra_tec_cd',
        'obra_capa_cd',
        'cartel_obra_id ',
        'tiene_colocacion',
        'empresa_origen_cd',
        'obra_ref_fisc_cd',
        'extra_observaciones',
        'provincia_id',
        'pais_cd',
        'kg_perfileria',
        'obra_cmpl',
        'obra_ind_cmpl',
        'obra_obs',
        'obra_crc'
    ]
    
    @api.onchange('obra_padre_id')
    def _onchange_obra_padre_id(self):
        """Hereda automáticamente los valores del proyecto padre al seleccionarlo."""
        if self.obra_padre_id:
            padre = self.obra_padre_id
            for field_name in self._fields:
                # Condiciones para copiar el campo:
                # - Está en FIELDS_TO_INCLUDE, O
                # - No está excluido y no es computado/relacionado
                if (
                    field_name in self.FIELDS_TO_INCLUDE 
                    and (
                        not self._fields[field_name].compute 
                        and not self._fields[field_name].related
                    )
                ):
                    _logger.warning(f"campo a copiar: {field_name}")
                    self[field_name] = padre[field_name]

    # --------------------------------------------------------------------------
    # FUNCIONES BASE DE ODOO
    # --------------------------------------------------------------------------
    
    @api.model
    def _name_search(self, name='', domain=None, operator='ilike', limit=100, order=None, name_get_uid=None):
        """Búsqueda por 'name' o 'obra_nr' en campos Many2one."""

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
    def create(self, vals):
        # Asignar la compañía si no se proporcionó
        if not vals.get('company_id'):
            vals['company_id'] = self.env.company.id

        
        # Generar número de obra secuencial
        if not vals.get('obra_nr'):
            next_value= self.env['ir.sequence'].next_by_code('custom.project.number')
            #_logger.warning(f"next_value: {next_value}")

            vals['obra_nr'] = next_value

        # Generar obra_nr único incluso si la secuencia es modificada
        if not vals.get('obra_nr'):
            while True:
                next_value = self.env['ir.sequence'].next_by_code('custom.project.number')
                existing = self.search_count([('obra_nr', '=', next_value)])
                if not existing:
                    vals['obra_nr'] = next_value
                    break
        
        # Crear cuenta analítica automáticamente
        if not vals.get('analytic_account_id'):
            analytic_account = self.env['account.analytic.account'].create({
                'name': vals.get('name'),
                'company_id': self.company_id.id,
                'plan_id': 1,
            })
            vals['analytic_account_id'] = analytic_account.id

        record = super(ProjectProject, self).create(vals)
        record._onchange_obra_padre_id()
        
        return record



    def write(self, vals):
            # Si se está cambiando el estado de obra, se actualiza la fecha a la fecha actual.
            if 'estado_obra_proyect' in vals:
                vals['obra_estd_fc_ulti_modi'] = fields.Date.context_today(self)
            return super(ProjectProject, self).write(vals)






