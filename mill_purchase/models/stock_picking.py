from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class StockPicking(models.Model):
    _inherit = "stock.picking"
    _description = "Stock Picking Purchase"

    truck_no = fields.Char("Truck No.")
    pcs = fields.Float("Pcs")
    bill_no =  fields.Char("Bill No.")
    heat_ids = fields.One2many('heat.heat','stock_picking_id',string = "Heats")

