from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    obra_nr = fields.Char(string="Número de Obra", readonly=False, copy=False,store=True)
    
    obra_padre_id = fields.Many2one(
        'project.project',
        string="Obra Padre",
        domain="[('company_id', 'in', allowed_company_ids)]",  # Filtra por compañías permitidas
        no_create=True
    )

    color_proyect = fields.Many2one(
        'project.color',
         string="Color proyecto",
         #ObraColoCd
    )


    estado_obra_proyect = fields.Many2one(
        'project.obraestado',
         string="Estado obra",
         #ObraEstado
    )

    obra_estd_fc_ulti_modi = fields.Date(
        string="Última Modif. Estado de Obra",
        readonly=True,
        help="Fecha en que se modificó por última vez el estado de la obra."
    )


    # CRM (x_studio_nv_linea)
    lnart_proyect = fields.Many2one(
        'project.lnarti',
         string="Ln Artic",
         #LnArtic
    )

    obratipo_proyect = fields.Many2one(
        'project.obratipo',
         string="Obra Tipo",
         #Obra tipo
    )


    obratipo_ubi = fields.Many2one(
        'project.ubic',
         string="Obra Ubicacion",
         #Obra tipo
    )


    cod_postal_proyect = fields.Integer(
        compute="_compute_cod_postal_proyect",
        string="Cod Postal",
    )


    ubi_area_proyect = fields.Integer(
        compute="_compute_ubi_area_proyect",
        string="Ubi Area",
    )

    nombre_carga_obra = fields.Char(
        string="Nombre de carga Obra:"
    )

    direccion = fields.Char(
        strign="Dirección"
    )

     # --------------------------------------------------------------------------
    # NUEVOS CAMPOS (Basados en las columnas que NO están marcadas como 'ya')
    # --------------------------------------------------------------------------

    # 1. Fecha de Aprobación de Presupuesto (ej. ObraFcAlta)
    fecha_aprobacion_presupuesto = fields.Date(
        string="Fecha Aprob. Presupuesto",
        compute="_compute_fecha_aprobacion_presupuesto",
        store=True,
        help="Fecha de aprobación de presupuesto (solo fecha, sin hora)"
    )

    # 2. Teléfonos y Fax (ObraTel1, ObraTel2, ObraFax1, ObraFax2)
    celular_1 = fields.Char(string="Celular 1")          # ObraTel1
    telefono_fijo = fields.Char(string="Teléfono Fijo")  # ObraTel2
    fax_1 = fields.Char(string="Fax 1")                  # ObraFax1
    fax_2 = fields.Char(string="Fax 2")                  # ObraFax2

    # 3. Tiempo proyectado (campo de ejemplo para “[[[[[tiempo proyectado]]]]]”)
    tiempo_proyectado = fields.Integer(string="Tiempo Proyectado")

    # 4. Observaciones (ObraObs)
    observaciones = fields.Text(string="Observaciones")

    # 5. Código Plus (ObraCdPlus)
    codigo_plus = fields.Char(string="Código Plus")

    # 6. Fecha Probable de Entrega (ObraFcEntrPact / ObraFcEntrRene)
    fecha_pactada_entrega = fields.Date(string="Fecha Pactada de Entrega")
    fecha_renegociada_entrega = fields.Date(string="Fecha Renegociada de Entrega")

    # 7. Vendedor / Jefe / Técnico / Capataz (ObraVendCd, ObraJefeCd, ObraTecCd, ObraCapaCd)
    obra_vend_cd = fields.Many2one(
        'project.syusro', 
        string="Vendedor", 
        help="Código de Vendedor"
    )
    obra_jefe_cd = fields.Many2one(
        'project.syusro', 
        string="Jefe", 
        help="Código de Jefe de Obra"
    )
    obra_tec_cd = fields.Many2one(
        'project.syusro', 
        string="Técnico", 
        help="Código de Técnico"
    )
    obra_capa_cd = fields.Many2one(
        'project.syusro', 
        string="Capataz", 
        help="Código de Capataz"
    )

    # 8. Cartel Obra (ObraCartEstd) CRM (x_studio_nv_cartel)
    cartel_obra = fields.Char(string="Cartel de Obra")

    # 9. Indica si tiene Colocación (ObraColoca) -> asumiendo S/N
    tiene_colocacion = fields.Selection([
        ('S', 'Sí'),
        ('N', 'No'),
    ], string="¿Tiene Colocación?")

    # 10. Empresa Origen (ObraEmprCd) - CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
    empresa_origen_cd = fields.Integer(
        string="Empresa Origen Código",
        compute="_compute_empresa_origen_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=1 NOA=2 GALVANIZADOS=3"
    )

    obra_ref_fisc_cd = fields.Integer(
        string="Empresa Origen Código",
        compute="_compute_obra_ref_fisc_cd",
        store=True,
        help="SI LA OBRA ES DE CRISTALIZANDO=4503 NOA=12873 GALVANIZADOS=13225"
    )
   
    # 11. Campo Adicional de Observaciones si se requiere
    #     (Si hubiera otra columna de Observaciones extra, se define aquí)
    extra_observaciones = fields.Text(string="Observaciones Extra")

    # 12. Campos de país y provincia si los tuvieras (PrvnCd, PaisCd) -> Asumimos guardarlos como Enteros
    # Reemplazar los campos prvn_cd y pais_cd por:
    provincia_id = fields.Many2one(
        'project.provincia',
        string="Provincia",
        help="Selecciona la provincia a la que pertenece el proyecto.",
    )
    pais_cd = fields.Char(
        string="Código de País",
        related="provincia_id.pais_cd",
        store=True,
        readonly=True,
        help="Código de país obtenido de la provincia."
    )

    # 13 Kilogramos de Perfileria CRM(x_studio_nv_kg_perfilera)
    kg_perfilería= fields.Integer(
        string="Kg de Perfileria"
    )

    obra_cmpl = fields.Integer(
        string="YA casi no se usa"
    )

    obra_ind_cmpl = fields.Integer(
        string="YA casi no se usa"
    )

    obra_obs = fields.Integer(
        string="YA casi no se usa"
    )

    obra_crc = fields.Integer(
            string="YA casi no se usa"
        )

    




    # --------------------------------------------------------------------------
    # RESTRICCIONES Y COMPUTES
    # --------------------------------------------------------------------------
    
    @api.depends('company_id')
    def _compute_empresa_origen_cd(self):
        for project in self:
            if project.company_id:
                # Toma el id de la empresa por defecto
                project.obra_ref_fisc_cd = project.company_id.id 
                
                # CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
                if project.company_id.id == 3:
                    # Cristalizando 
                    project.obra_ref_fisc_cd = 1
                elif project.company_id.id == 2:
                    # Noa Aberturas
                    project.obra_ref_fisc_cd = 2
                elif project.company_id.id == 4:
                    # Galvanizados del Norte
                    project.obra_ref_fisc_cd = 3
                
            else:
                project.obra_ref_fisc_cd = False



    @api.depends('company_id')
    def _compute_obra_ref_fisc_cd(self):
        for project in self:
            if project.company_id:
                # Toma el id de la empresa por defecto
                project.empresa_origen_cd = project.company_id.id 
                
                # CRISTALIZANDO=4503, NOA=12873, GALVANIZADOS=13225
                if project.company_id.id == 3:
                    # Cristalizando 
                    project.empresa_origen_cd = 4503
                elif project.company_id.id == 2:
                    # Noa Aberturas
                    project.empresa_origen_cd = 12873
                elif project.company_id.id == 4:
                    # Galvanizados del Norte
                    project.empresa_origen_cd = 13225
                
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
    def _compute_ubi_area_proyect(self):
        for record in self:
            record.ubi_area_proyect = record.obratipo_ubi.ubic_area_cd if record.obratipo_ubi else ''

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
        
        return super(ProjectProject, self).create(vals)



    def write(self, vals):
            # Si se está cambiando el estado de obra, se actualiza la fecha a la fecha actual.
            if 'estado_obra_proyect' in vals:
                vals['obra_estd_fc_ulti_modi'] = fields.Date.context_today(self)
            return super(ProjectProject, self).write(vals)






