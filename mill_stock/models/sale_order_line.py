from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Stock Sale Order Line"

    grade_id = fields.Many2one("material.grade","Grade")