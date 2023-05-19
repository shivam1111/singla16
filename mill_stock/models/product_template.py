from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = "Mill Order Product Template"

    grade_id = fields.Many2one("material.grade",string = "Grade")