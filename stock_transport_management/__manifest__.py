# -*- coding: utf-8 -*-
{
    'name': "Stock Transport Management",
    'version': '10.0.2.0.0',
    'summary': """Manage Stock Transport Management With Ease""",
    'description': """This Module Manage Transport Management Of Stocks""",
    'author': "Appscomp",
    'company': 'Appscomp',
    'website': "https://www.Appscomp.com",
    'category': 'Warehouse',
    'depends': ['base', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/transport_vehicle_view.xml',
        'views/transport_vehicle_status_view.xml',
        'views/transportation_sale_order_view.xml',
        'views/transport_warehouse_view.xml',
        #'views/gate_view.xml',
        #'views/transport_wizard_view.xml',
        #'views/transport_report.xml',
    ],
    
    'license': 'AGPL-3',
    'installable': True,
    #'auto_install': False,
    #'application': False,
}
