# -*- coding: utf-8 -*-


{
    'name': 'Barcode scanning support for sale and Purchase',
    'version': '13.0.1.0.0',
    'category': 'Sales',
    'summary': 'This module will help you to use barcode scanner in sales and purchase.',
    'depends': ['purchase', 'sale_management'],
    'demo': [],
    'data': [
        'views/sale_order_line.xml',
        'views/purchase_order_line.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'qweb': [],
    'license': 'AGPL-3',
}
