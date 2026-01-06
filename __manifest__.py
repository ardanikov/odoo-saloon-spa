# -*- coding: utf-8 -*-
{
    'name': "Salon",

    'summary': "Aplikasi Salon",

    'description': """
Long description of module's purpose
    """,

    'author': "PT Docker Compose",
    'website': "https://www.dockercompose.id",
    'category': 'Uncategorized',
    'version': '18.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'account', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'data/ir_sequence_data.xml',
        'views/menu_salon.xml',
        'views/appointment.xml',
        'views/pelanggan.xml',
        'views/product_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

