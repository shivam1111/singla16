# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Mill Stock',
    'version': '1.1',
    'category': 'Mill Management',
    'depends' : ['base','mill_order','stock_picking_purchase_order_link'],
    'description': """
    Mill Sales Order
    """,
    'data': [
        'data/stock_data.xml',
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/material_grade.xml',
        'views/heat_heat.xml',
        'views/stock_menus.xml',
        'views/sale_order_line_view.xml',
        'views/product_template.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}
