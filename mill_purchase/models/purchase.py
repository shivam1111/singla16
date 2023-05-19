from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Mill Purchase Order"

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

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    _description = "Purchase Order Line Mill"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id.product_tmpl_id.grade_id:
                self.order_id.grade_id = line.product_id.product_tmpl_id.grade_id
    @api.depends('order_id.net_rate')
    def _compute_price_unit_and_date_planned_and_name(self):
        self.price_unit = self.order_id.net_rate