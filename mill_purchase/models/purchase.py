from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.float_utils import  float_round
from odoo.tools import get_lang,DEFAULT_SERVER_DATETIME_FORMAT
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Mill Purchase Order"

    @api.depends('order_line', 'order_line.product_qty', 'order_line.qty_received')
    def _compute_total_qty(self):
        for po in self:
            if po._origin.id:
                total_qty = 0.0
                qty_rcvd = 0.0
                for line in po.order_line:
                    if line._origin.id:
                        total_qty+= line.product_qty
                        qty_rcvd+= line.qty_received
                po.total_qty = total_qty
                po.qty_rcvd = qty_rcvd
            else:
                po.total_qty=0
                po.qty_rcvd=0

    @api.depends("basic_rate",
                 "extra_rate")
    def _compute_net_rate(self):
        for order in self:
            order.net_rate = order.basic_rate + order.extra_rate


    #TODO Merge Broker Module with Purchase Module
    #TODO Add Basic Rate and Final Rate to the Report of Brokerage
    heats = fields.Float("Heats")
    basic_rate = fields.Float("Basic Rate")
    broker_id = fields.Many2one('res.partner','Broker',domain = [('is_broker','=',True)])
    extra_rate = fields.Float('Extra Rate')
    net_rate = fields.Float(string = "Net Rate", compute = '_compute_net_rate')
    grade_id = fields.Many2one('material.grade','Material Grade')
    total_qty = fields.Float(name="Total Qty",compute="_compute_total_qty",store=True)
    qty_rcvd = fields.Float(name="Total Received",compute="_compute_total_qty",store=True)

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    _description = "Purchase Order Line Mill"


    @api.depends('product_qty', 'product_uom','order_id.net_rate')
    def _compute_price_unit_and_date_planned_and_name(self):
        super(PurchaseOrderLine,self)._compute_price_unit_and_date_planned_and_name()
        for line in self:
            line.price_unit = line.order_id.net_rate

    def _suggest_quantity(self):
        '''
        Suggest a minimal quantity based on the seller
        '''
        for line in self:
            line.product_qty = (line.order_id.heats or 0.00) * 7.5