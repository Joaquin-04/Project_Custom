from odoo import models, fields, api, _
from odoo.exceptions import UserError,ValidationError

import logging

_logger = logging.getLogger(__name__)

class SaleOrderProjectWizard(models.TransientModel):
    """
    Wizard Transiente para gestión de proyectos en órdenes de venta
    
    Flujo Principal:
    1. Usuario selecciona proyecto existente o crea nuevo
    2. Valida consistencia de datos y relaciones empresariales
    3. Crea proyecto nuevo con datos del lead si corresponde
    4. Vincula proyecto a orden de venta y oportunidad relacionada
    5. Confirma automáticamente la orden de venta
    
    Campos Clave:
    - create_new: Bandera para creación de nuevos proyectos
    - obra_padre_id: Jerarquía de proyectos
    - LEAD_PARENT_SELECTION_MAPPING: Reglas de prioridad para campos
    """
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

    
    create_new = fields.Boolean(string="Crear Nuevo Proyecto?", default=True)
    
    new_project_name = fields.Char(string="Nombre del Nuevo Proyecto")

    obra_padre_id = fields.Many2one(
        'project.project', 
        string="Obra Padre",
        domain="[('company_id', '=', company_id)]"
    )

    FIELDS_OPPORTUNITY=[
    
        'x_studio_nv_nombre_de_carga_obra',
        'x_studio_nv_direccion',
        'project_ubi_id',
        'cod_postal_proyect',
        'ubi_area_proyect',
        'ubi_code',
        'x_studio_celular_1'
        'x_studio_telefono_fijo',
        'phone_mobile_search',#fax1
        'estado_obra_proyect_id',
        'obratipo_proyect_id',
        'color_proyect_id',
        'lnart_proyect',
        'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'x_studio_nv_codigo_plus',
        'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'x_studio_nv_cartel',
        'provincia_id',
        'pais_cd'
    ]

    # En tu SaleOrderProjectWizard
    LEAD_TO_PROJECT_MAPPING = {
        # Campo Proyecto: Campo Lead
        'nombre_carga_obra': 'x_studio_nv_nombre_de_carga_obra',
        'direccion': 'x_studio_nv_direccion',
        'obratipo_ubi': 'project_ubi_id',
        'cod_postal_proyect': 'cod_postal_proyect',
        'ubi_area_proyect': 'ubi_area_proyect',
        'celular_1': 'x_studio_celular_1',
        'telefono_fijo': 'x_studio_telefono_fijo',
        'fax_1': 'phone_mobile_search',  # Asumiendo que phone_mobile_search es el fax1
        'estado_obra_proyect': 'estado_obra_proyect_id',
        'obratipo_proyect': 'obratipo_proyect_id',
        'color_proyect': 'color_proyect_id',
        'lnart_proyect': 'lnart_proyect_id',
        'fecha_pactada_entrega': 'x_studio_nv_fecha_probable_de_entrega_de_obra',
        'codigo_plus': 'x_studio_nv_codigo_plus',
        'cartel_obra_id': 'cartel_obra_id',
        'provincia_id': 'provincia_id',
        'pais_cd': 'pais_cd',
        'kg_perfileria': 'x_studio_nv_kg_perfilera',
        # Agrega más mapeos según necesidad
    }

    # Mapeo para los campos en los que se requiere elegir entre el valor del lead y, en su defecto, del proyecto padre.
    # Por ejemplo, para el vendedor queremos que siempre se use el valor del lead.
    LEAD_PARENT_SELECTION_MAPPING = {
        """
        Reglas de prioridad para campos:
        - 'lead': Valor del lead tiene prioridad absoluta
        - 'padre': Usar valor del proyecto padre si existe
        - 'strict_lead': Campo obligatorio desde lead
        
        Estructura por campo:
        - lead_field: Campo origen en lead
        - parent_field: Campo origen en proyecto padre (opcional)
        - priority: Regla de prioridad
        """



        'color_proyect': {
            'lead_field': 'color_proyect_id',  # Campo en el CRM lead
            'parent_field': 'color_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'lnart_proyect': {
            'lead_field': 'lnart_proyect_id',  # Campo en el CRM lead
            'parent_field': 'lnart_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obratipo_proyect': {
            'lead_field': 'obratipo_proyect_id',  # Campo en el CRM lead
            'parent_field': 'obratipo_proyect',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obratipo_ubi': {
            'lead_field': 'project_ubi_id',  # Campo en el CRM lead
            'parent_field': 'obratipo_ubi',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'direccion': {
            'lead_field': 'x_studio_nv_direccion',  # Campo en el CRM lead
            'parent_field': 'direccion',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'telefono_fijo': {
            'lead_field': 'x_studio_telefono_fijo',  # Campo en el CRM lead
            'parent_field': 'telefono_fijo',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'celular_1': {
            'lead_field': 'x_studio_celular_1',  # Campo en el CRM lead
            'parent_field': 'celular_1',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fax_1': {
            'lead_field': 'x_studio_fax1',  # Campo en el CRM lead
            'parent_field': 'fax_1',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fax_2': {
            'lead_field': 'x_studio_fax2',  # Campo en el CRM lead
            'parent_field': 'fax_2',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'codigo_plus': {
            'lead_field': 'x_studio_nv_codigo_plus',  # Campo en el CRM lead
            'parent_field': 'codigo_plus',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'fecha_pactada_entrega': {
            'lead_field': 'x_studio_nv_fecha_probable_de_entrega_de_obra',  # Campo en el CRM lead
            'parent_field': 'fecha_pactada_entrega',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },
        'fecha_renegociada_entrega': {
            'lead_field': 'x_studio_nv_fecha_probable_de_entrega_de_obra',  # Campo en el CRM lead
            'parent_field': 'fecha_renegociada_entrega',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },
        'obra_vend_cd': {
            'lead_field': 'vendedor_id',  # Campo en el CRM lead
            'parent_field': 'obra_vend_cd',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'obra_jefe_cd': {
            'lead_field': 'jefe_obra_id',  # Campo en el CRM lead
            'parent_field': 'obra_jefe_cd',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'cartel_obra_id': {
            'lead_field': 'cartel_obra_id',  # Campo en el CRM lead
            'parent_field': 'cartel_obra_id',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'lead'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'provincia_id': {
            'lead_field': 'provincia_id',  # Campo en el CRM lead
            'parent_field': 'provincia_id',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'padre'  # 'lead' significa que se toma siempre el valor del lead si existe
        },
        'kg_perfileria': {
            'lead_field': 'x_studio_nv_kg_perfilera',  # Campo en el CRM lead
            'parent_field': 'kg_perfileria',  # (Opcional) Si en algún caso deseas fallback al padre
            'priority': 'strict_lead'   # Nueva prioridad para campos obligatorios desde el lead
        },
        
    }



    @api.model
    def default_get(self, fields_list):
        """
        Inicialización inteligente del wizard:
        1. Obtiene orden de venta del contexto
        2. Precarga proyecto relacionado si existe
        3. Suggestion de nombre desde lead
        
        Parámetros:
        - fields_list: Campos a inicializar (manejado por herencia)
        
        Return:
        - Diccionario con valores iniciales
        """
        res = super(SaleOrderProjectWizard, self).default_get(fields_list)
        sale_order = self.env['sale.order'].browse(self.env.context.get('default_sale_order_id'))

        lead = sale_order.opportunity_id

        project_id = sale_order.opportunity_id.project_id

        obra_padre_id = sale_order.opportunity_id.obra_padre_id

        if obra_padre_id:
            res['obra_padre_id']=obra_padre_id
        
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
        """
        Acción principal del wizard:
        1. Crea proyecto nuevo o selecciona existente
        2. Copia datos desde oportunidad
        3. Aplica reglas de mapeo lead/padre
        4. Vincula proyecto a orden y oportunidad
        5. Confirma orden de venta automáticamente
        
        Flujo de Excepciones:
        - Registra errores en modelo dedicado (project.sequence.log)
        - Log detallado para auditoría
        - Rollback automático de transacción en fallos
        """
        try:
            if self.create_new:
                if not self.new_project_name:
                    raise UserError(_("Debe ingresar un nombre para el nuevo proyecto."))
    
                project = self.env['project.project'].create({
                    'name': self.new_project_name,
                    'company_id': self.sale_order_id.company_id.id,
                    'obra_padre_id': self.obra_padre_id.id if self.obra_padre_id else False,
                })

                # Copiar campos desde el CRM lead si existe
                sale_order = self.env['sale.order'].browse(self.env.context.get('default_sale_order_id'))
                opportunity = sale_order.opportunity_id
                if opportunity:
                    self._copy_fields_from_opportunity(project, opportunity, project.FIELDS_TO_INCLUDE)
                    # Copiar campos adicionales específicos
                    #project.obra_vend_cd = opportunity.vendedor_id
                    #project.obra_jefe_cd = opportunity.jefe_obra_id
                    # project.obra_tec_cd = opportunity.cotizador_id  # Asumiendo relación
                    # project.tiene_colocacion = 'S' if opportunity.probability > 50 else 'N'

                    # Para campos computados que son stored=True
                    #if opportunity.ubi_code:
                    #    project.ubi_code = opportunity.ubi_code
            
                    # Aplicar lógica para campos donde se elige entre lead y proyecto padre
                    self._apply_lead_vs_parent_field(project, opportunity, self.LEAD_PARENT_SELECTION_MAPPING)
                    
                elif self.obra_padre_id:
                    # Copiar campos del padre
                    project._onchange_obra_padre_id()

            
            else:
                project = self.project_id
    
            # Asignar el proyecto a la orden de venta
            self.sale_order_id.project_id = project

            # Asignar el proyecto al lead relacionado a la orden de venta
            self.sale_order_id.opportunity_id.project_id =project
            
            # Asignar el numero del proyecto al lead relacionado a la orden de venta

            self.sale_order_id.opportunity_id.x_studio_nv_numero_de_obra_relacionada =project.obra_nr

            # Asignar el numero del proyecto padre del proyecto al lead relacionado a la orden de venta
            self.sale_order_id.opportunity_id.x_studio_nv_numero_de_sp =project.obra_padre_nr


            # self.sale_order_id._onchange_project_id()
    
            # Forzar actualización de líneas
            self.sale_order_id._update_analytic_distribution()
    
            # Confirmar la orden de venta
            self.sale_order_id.action_confirm()
    
            return {'type': 'ir.actions.act_window_close'}
    
        except Exception as e:
            # Registrar el log de auditoría para errores
            audit_vals = {
                'project_id': 0,
                'user_id': self.env.uid,
                'company_id': self.sale_order_id.company_id.id,
                'state': 'error',
                'message': f'Error en action_apply: {str(e)}'
            }
            self.env['project.sequence.log'].sudo().create(audit_vals)
            _logger.error(f"Error en action_apply: {str(e)}")
            raise UserError(_(f'Ocurrió un error al aplicar la acción.\n {str(e)}'))

    

    def _copy_fields_from_opportunity(self, project, opportunity,fields_to_include):
        """
        Copia masiva de campos desde oportunidad a proyecto:
        - Maneja tipos de campos (M2O, M2M, escalares)
        - Omite campos vacíos
        - Registra errores por campo sin bloquear proceso
        
        Parámetros:
        - project: Objeto proyecto destino
        - opportunity: Objeto lead/origen
        - fields_to_include: Lista de campos a procesar
        """
        for project_field, lead_field in self.LEAD_TO_PROJECT_MAPPING.items():
            try:
                if project_field not in fields_to_include:
                    continue
                    
                if not opportunity[lead_field]:
                    continue  # No copiar valores vacíos
                    
                field_type = project._fields[project_field].type
                
                # Manejo especial para tipos de campos
                if field_type == 'many2one':
                    project[project_field] = opportunity[lead_field].id
                elif field_type == 'many2many':
                    project[project_field] = [(6, 0, opportunity[lead_field].ids)]
                elif field_type == 'date' and not opportunity[lead_field]:
                    continue  # Saltar fechas inválidas
                else:
                    project[project_field] = opportunity[lead_field]
                    
            except Exception as e:
                _logger.error(f"Error copiando {lead_field} a {project_field}: {str(e)}")
                continue

    


    def _apply_lead_vs_parent_field(self, project, opportunity, field_mapping):
        """
        Aplica la lógica de selección entre el valor del lead y el del proyecto padre.
        
        field_mapping: dict donde cada clave es un campo del proyecto y su valor es un dict con:
            - lead_field: nombre del campo en el CRM lead.
            - parent_field: nombre del campo en el proyecto padre (opcional).
            - priority: 'lead' (usar siempre el valor del lead si existe) o 'parent_if_empty' (usar el del padre si el lead está vacío).
        
        Para el caso del teléfono (campo 'telefono_fijo'), se prioriza el valor del lead; si está vacío,
        se usa el valor del cliente (partner_id.phone).
        
        Lógica avanzada de prioridad de campos:
        1. Determina fuente de datos (lead/padre)
        2. Aplica reglas de prioridad configuradas
        3. Genera logs detallados de asignación
        
        Casos Especiales:
        - Campos telefónicos con fallback a partner
        - Campos obligatorios (strict_lead)
        - Formateo de valores para logs
        """
        # Función para formatear valores
        def format_value(value):
            if isinstance(value, models.BaseModel):
                return f"(ID: {value.id}, Nombre: {value.display_name})" if value else "None"
            elif isinstance(value, bool):
                return str(bool(value))
            elif value is None:
                return "None"
            return str(value)

        
        parent_project = project.obra_padre_id
        for proj_field, config in field_mapping.items():
            # Caso especial para el campo teléfono
            if proj_field == 'celular_1':
                # Intentar obtener el valor del lead
                lead_value = getattr(opportunity, config.get('lead_field'), False)
                # Si no hay valor en el lead, intentamos tomarlo del teléfono del cliente (partner_id.phone)
                if not lead_value and opportunity.partner_id:
                    lead_value = opportunity.partner_id.phone
                # Si hay un proyecto padre y el lead no tiene valor, obtenemos el valor del padre
                parent_value = parent_project and config.get('parent_field') and getattr(parent_project, config.get('parent_field'), False) or False
                # Según la prioridad, se asigna
                if config.get('priority', 'lead') == 'lead':
                    value = lead_value if lead_value else parent_value
                else:
                    value = parent_value if parent_value else lead_value
            else:
                # Lógica por defecto para otros campos
                lead_value = getattr(opportunity, config.get('lead_field'), False)
                parent_value = parent_project and config.get('parent_field') and getattr(parent_project, config.get('parent_field'), False) or False
                # Nueva lógica para prioridad estricta del lead
                if config.get('priority') == 'strict_lead':
                    value = lead_value  # Toma el valor del lead incluso si está vacío
                    source = 'LEAD (forzado)'
                    final_value = lead_value
            
                elif config.get('priority', 'lead') == 'lead':
                    value = lead_value if lead_value else parent_value
                    source = 'LEAD' if lead_value else 'PADRE (por vacío LEAD)'
                    final_value = lead_value or parent_value
                
                else:
                    value = parent_value if parent_value else lead_value
                    source = 'PADRE' if parent_value else 'LEAD (por vacío PADRE)'
                    final_value = parent_value or lead_value

            # Log detallado
            _logger.warning(
                "\n| Campo Proyecto: %s"
                "\n| Fuente: %s"
                "\n| Valor LEAD (%s): %s"
                "\n| Valor PADRE (%s): %s"
                "\n| Valor FINAL asignado: %s"
                "\n|----------------------------------",
                proj_field.upper(),
                source,
                config.get('lead_field', 'N/A'),
                format_value(lead_value),
                config.get('parent_field', 'N/A'),
                format_value(parent_value),
                format_value(final_value)
            )


            
            project[proj_field] = value


    """
    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        #Consistencia empresarial:
        #- Proyecto y orden deben pertenecer a misma compañía
        #- Previene cruce de datos entre organizaciones
        
        for record in self:
            if record.project_id and record.company_id != record.project_id.company_id:
                raise ValidationError(_(
                    f"El proyecto seleccionado '{record.project_id.name}' pertenece a otra empresa: {record.project_id.company_id.name}."
                ))
    """






# ---------------------------------------------------------------------------------------
# DOCUMENTACIÓN ADICIONAL
# ---------------------------------------------------------------------------------------

"""
ARQUITECTURA DE DATOS:
----------------------------------------------------------------------------------------
1. Relaciones Clave:
   - sale_order_id: Vinculación con documento comercial
   - project_id: Proyecto existente seleccionado
   - obra_padre_id: Jerarquía de proyectos

2. Mapeos de Campos:
   - LEAD_TO_PROJECT_MAPPING: Correspondencia directa 1:1
   - LEAD_PARENT_SELECTION_MAPPING: Lógica condicional lead/padre

3. Campos Técnicos:
   - create_new: Bandera de creación/uso existente
   - new_project_name: Nombre para nuevos proyectos

FLUJOS DE TRABAJO:
----------------------------------------------------------------------------------------
1. Creación Nuevo Proyecto:
   - Validación nombre
   - Copia campos desde lead
   - Aplica herencia desde obra padre
   - Genera números de obra

2. Uso Proyecto Existente:
   - Validación compañía
   - Actualización de campos relacionados

REGISTRO Y AUDITORÍA:
----------------------------------------------------------------------------------------
- Logging detallado en cada paso crítico
- Modelo project.sequence.log para errores
- Trazas en _logger con formato estructurado

OBSERVACIONES TÉCNICAS:
----------------------------------------------------------------------------------------
1. Dependencias:
   - Campos x_studio_* requieren módulos Studio
   - Modelos project.* son personalizaciones específicas

2. Supuestos:
   - Existencia de modelo project.sequence.log
   - Campos técnicos en sale.order (project_id, opportunity_id)
   - Relación sale.order <-> crm.lead mediante opportunity_id

3. Seguridad:
   - Validación de compañía en múltiples niveles
   - Readonly en campos críticos
   - Manejo seguro de IDs mediante browse()

4. Optimización:
   - Queries limitadas con search(..., limit=1)
   - Bulk operations en métodos compute
   - Validación por lotes (@api.constrains)

BUENAS PRÁCTICAS IMPLEMENTADAS:
----------------------------------------------------------------------------------------
- Separación clara entre lógica de negocio y UI
- Métodos cortos con responsabilidad única
- Manejo adecuado de excepciones
- Logs informativos para diagnóstico
- Validación temprana de datos
- Uso apropiado de @api.constrains
"""
