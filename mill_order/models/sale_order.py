from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class OrderDeliveryLine(models.Model):
    _name = "order.delivery.line"
    _description = "Sale Order Delivery Line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('order.delivery.line') or _("New")
        return super().create(vals_list)

    name = fields.Char("Name",required=True,default=lambda self: _('New'))
    size = fields.Char("Size")
    order_id = fields.Many2one(comodel_name = "sale.order",required=True,string = "Sale Order Line",
                              ondelete='cascade', index=True, copy=False)
    line_id = fields.Many2one(comodel_name = "sale.order.line",required=True,
                              domain = "[('order_id','=',parent.id)]")

    completed_qty = fields.Float("Completed Qty")
    invoice_no = fields.Integer("Invoice No.")
    remarks = fields.Char("Remarks")


class SaleOrder(models.Model):
    _inherit="sale.order"
    _description = "Mill Order"

    @api.depends("ingot_price",
                 "rolling","extra_rate")
    def _compute_net_rate(self):
        for order in self:
            order.net_rate = order.ingot_price+order.extra_rate+order.rolling

    def _compute_quantities(self):
        for order in self:
            total_qty = 0
            delivered_qty = 0
            for line in order.order_line:
                total_qty+= line.product_uom_qty
                delivered_qty+=line.qty_delivered
            order.balance_qty = total_qty-delivered_qty
            order.total_qty = total_qty
            order.delivered_qty = delivered_qty

    @api.onchange('order_line')
    def onchange_line_ids(self):
        for order in self:
            sizes_list = map(lambda x:x.name and x.product_template_id.name or '',order.order_line)
            order.size = ' | '.join(sizes_list) or "Size Unknown"

    ingot_price = fields.Float(string="Ingot Price")
    size = fields.Char("Size")
    rolling = fields.Float(string = "Rolling",default = 0)
    extra_rate = fields.Float(string = "Extra Rate",default = 0)
    loading = fields.Boolean(string = "Loading Inclusive")
    net_rate = fields.Float(string = "Net Rate", compute = '_compute_net_rate')
    balance_qty = fields.Float(string = "Balance Qty",compute = "_compute_quantities",store=True)
    delivered_qty = fields.Float(string = "Completed Qty",compute = "_compute_quantities",store=True)
    total_qty = fields.Float(string = "Ordered Qty",compute = "_compute_quantities",store=True)
    delivery_line = fields.One2many(comodel_name="order.delivery.line", inverse_name="order_id", string="Delivery Line")
    po_id = fields.Many2one("purchase.order",'Purchase Order')

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Mill Order Line"


    cut_length = fields.Char("Cut Length")
    tolerance = fields.Char("Tolerance")

    @api.depends('order_id.net_rate')
    def _compute_price_unit(self):
        self.price_unit = self.order_id.net_rate

    @api.depends(
        'qty_delivered_method',
        'order_id.delivery_line',
        'order_id.delivery_line.completed_qty'
    )
    def _compute_qty_delivered(self):
        """
            line.is_expense will always be false hence the delivery method will always be manual
        """
        super(SaleOrderLine, self)._compute_qty_delivered()
        for line in self:
            delivery_lines = line.env['order.delivery.line'].search([('line_id','=',line._origin.id)])
            qty = 0
            for i in delivery_lines:
                qty+= i.completed_qty
            line.qty_delivered = qty
