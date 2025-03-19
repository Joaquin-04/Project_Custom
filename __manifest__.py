{
    'name': 'Custom Project Management',
    'version': '1.0',
    'summary': 'Gestión personalizada de proyectos con integración de cuenta analítica',
    'author': 'TuNombre',
    'depends': [
        'project',
        'sale',
        'purchase',
        'stock',
        'material_reservation',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        #SEcuencia
        'data/ir_sequence_data.xml',
        #Wizards
        'views/sale_order_project_wizard_view.xml',
        'views/project_change_obra_wizard_view.xml',
        
        #Vistas
        
        'views/sale_order_views.xml',
        'views/project_views.xml',
        'views/stock_picking_views.xml',
        'views/crm_lead_view.xml',
        'views/project_color_views.xml',
        'views/project_obra_estado_views.xml',
        'views/project_provincia_views.xml',
        'views/project_LnArti_views.xml',
        'views/project_ObraTipo_views.xml',
        'views/project_Ubi_views.xml',
        'views/syusro_views.xml',
        'views/project_cartel_obra_views.xml',
        # Auditoria
        'views/project_sequence_log_views.xml',
        
        'views/studio_extends.xml',
        
        
    ],
    'installable': True,
    'application': True,
}
