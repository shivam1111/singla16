# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Mill Purchase',
    'version': '1.1',
    'category': 'Mill Management',
    'depends' : ['base','product','stock','purchase','mill_stock'],
    'description': """
Installation Instructions
==========================

    """,
    'data': [
        'views/purchase_order.xml',
        'views/res_partner.xml',
        'views/stock_picking_view.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}
