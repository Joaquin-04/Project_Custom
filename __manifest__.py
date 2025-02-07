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
    ],
    'installable': True,
    'application': True,
}
