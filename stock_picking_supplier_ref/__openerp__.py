# -*- coding: utf-8 -*-

{
    'name': 'Stock Picking Supplier Reference',
    'summary': 'Stock Picking Supplier Reference',
    'description': '''
    Adds a supplier reference field inside supplier's pickings ans allows
    search for this reference.''',
    #'author': 'Trey (www.trey.es)',
    'license': 'AGPL-3',
    #'website': 'https://www.trey.es',
    'category': 'Stock',
    'version': '8.0.1.0.0',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'views/stock_picking.xml',
    ],
    'installable': True,
}
