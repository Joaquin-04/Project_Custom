{
    'name': 'Custom Project Management',
    'version': '1.0',
    'summary': 'Gestión personalizada de proyectos con integración de cuenta analítica',
    'author': 'TuNombre',
    'depends': ['project', 'sale', 'purchase', 'stock'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/project_views.xml',
        'views/res_config_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
