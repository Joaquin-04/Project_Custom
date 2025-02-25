<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="view_project_form_inherit_extras" model="ir.ui.view">
        <field name="name">project.project.form.inherit.extras</field>
        <field name="model">project.project</field>
        <field name="inherit_id" ref="project.edit_project"/>
        <field name="priority" eval="331"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Extras">
                    <group string="Información de Obra">
                        <field name="obra_nr"/>
                        <field name="obra_padre_id"
                               domain="[('company_id', 'in', allowed_company_ids)]"
                               context="{'allowed_company_ids': allowed_company_ids}"
                               options="{'no_create':True,'no_create_edit':True}"/>
                        <field name="color_proyect"
                               options="{'no_create':True,'no_create_edit':True}"/>
                        <field name="estado_obra_proyect"
                               options="{'no_create':True,'no_create_edit':True}"/>
                        <field name="obra_estd_fc_ulti_modi"/>
                        <field name="lnart_proyect"
                               options="{'no_create':True,'no_create_edit':True}"/> 
                        <field name="obratipo_proyect"
                               options="{'no_create':True,'no_create_edit':True}"/> 
                        <field name="obratipo_ubi"
                               options="{'no_create':True,'no_create_edit':True}"/>
                        <field name="cod_postal_proyect"/>
                        <field name="ubi_area_proyect"/>
                        <field name="kg_perfileria"/>
                        <field name="nombre_carga_obra"/>
                        <field name="direccion"/>
                    </group>
                    
                    <group string="Fechas y Contactos">
                        <field name="fecha_aprobacion_presupuesto"/>
                        <field name="celular_1"/>
                        <field name="telefono_fijo"/>
                        <field name="fax_1"/>
                        <field name="fax_2"/>
                        <field name="tiempo_proyectado"/>
                    </group>
                    
                    <group string="Observaciones y Códigos">
                        <field name="observaciones" style="width: 100%"/>
                        <field name="extra_observaciones" style="width: 100%"/>
                        <field name="codigo_plus"/>
                        <field name="obra_ref_fisc_cd"/>
                    </group>
                    
                    <group string="Fechas de Entrega y Empresa">
                        <field name="fecha_pactada_entrega"/>
                        <field name="fecha_renegociada_entrega"/>
                        <field name="cartel_obra"/>
                        <field name="tiene_colocacion"/>
                        <field name="empresa_origen_cd"/>
                    </group>
                    
                    <group string="Ubicación">
                        <field name="provincia_id"
                               options="{'no_create':True,'no_create_edit':True}"/> 
                        <field name="pais_cd"/>
                    </group>
                    
                    <group string="Responsables">
                        <field name="obra_vend_cd"/>
                        <field name="obra_jefe_cd"/>
                        <field name="obra_tec_cd"/>
                        <field name="obra_capa_cd"/>
                    </group>

                    <group string="Relaciones">
                        <field name="sale_order_ids"/>
                        <field name="lead_ids"/>
                        <field name="stock_picking_ids"/>
                    </group>
                    
                    <group string="Campos Legacy" col="4" invisible="1">
                        <field name="obra_cmpl"/>
                        <field name="obra_ind_cmpl"/>
                        <field name="obra_obs"/>
                        <field name="obra_crc"/>
                    </group>
                    
                </page>
            </xpath>
            
        </field>
    </record>
</odoo>