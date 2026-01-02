# -*- coding: utf-8 -*-
{
    'name': "Salon",

    'summary': "Aplikasi Salon",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '18.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/templates.xml',
        'data/sequence.xml',
        'views/menu_salon.xml',
        'views/pelanggan.xml',
        'views/terapis.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

