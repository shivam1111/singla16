# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Mill Order',
    'version': '1.1',
    'category': 'Mill Management',
    'depends' : ['base','sale','product','sale_stock','stock'],
    'description': """
Installation Instructions
==========================

First Install only the following modules in order

* Sale
* Purchase
* Invoicing
* Contacts
* Discuss
* Inventory
* Mill Sales Order (If installed before inventory, delivered qty will not work)
* Mill Stock

Other Settings
==============
* Switch on Variants in Sale Module
* Switch on Variants Matrix in Sale Module
* Switch on Storage locations in inventory
* While Adding Product 
    * Add name,attribute - edges (Sharp,Round). Also tick "Order Grid Entry" 
* Each Flat Bar Size will be a separate product wth attribute edge product attribute and its values
* Enable "Lock Confirmed Sales in Sales Order Module Settings
    
    """,
    'data': [
        "views/mill_order_menu.xml",
        "views/sale_order_views.xml",
        "views/product_template.py.xml",
        "data/ir_sequence_data.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'LGPL-3',
}
