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
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/project_views.xml',
        'views/stock_picking_views.xml',
        'views/crm_lead_view.xml',
        'views/sale_order_project_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
