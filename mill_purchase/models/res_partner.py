from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Mill Broker"

    is_broker = fields.Boolean('Is Broker')