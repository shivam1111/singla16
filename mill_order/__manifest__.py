# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Mill Order',
    'version': '1.1',
    'category': 'Mill Management',
    'depends' : ['base','sale'],
    'description': """
    Mill Sales Order
    """,
    'data': [
        "views/sale_order_views.xml",
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}
