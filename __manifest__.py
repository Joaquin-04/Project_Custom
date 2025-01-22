{
    'name': 'Custom Project Management',
    'version': '1.0',
    'summary': 'Gestión personalizada de proyectos con integración de cuenta analítica',
    'author': 'TuNombre',
    'depends': ['project', 'sale', 'purchase', 'stock'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/res_config_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
