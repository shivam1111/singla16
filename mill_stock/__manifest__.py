# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Mill Stock',
    'version': '1.1',
    'category': 'Mill Management',
    'depends' : ['base','sale'],
    'description': """
    Mill Sales Order
    """,
    'data': [
        'data/stock_data.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}
