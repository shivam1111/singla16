from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Mill Order Product Template"

# TODO Add grade_id field to finish products (FT size) so that when selected in sales order line the grade will be updated automatically

    raw_finish = fields.Selection(
        selection=[
            ('finish', 'Finish Product'),
            ('raw', 'Raw Material'),
        ],
        string='Finished/Raw Material ',
        tracking = True
    )
