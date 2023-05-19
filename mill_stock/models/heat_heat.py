from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class CompositionLine(models.Model):
    _inherit = "composition.line"
    _description =" Heat Composition Line"

    heat_id = fields.Many2one('heat.heat','Heat')

class IngotSize(models.Model):
    _name = "ingot.size"
    _description = "Ingot Size"

    name = fields.Char('Ingot Size')

class InclusionRatingLine(models.Model):
    _name = "inclusion.rating.line"
    _description = "Inclusion Rating Line"

    type = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], string="Inclusion Type")
    thin = fields.Char('Thin')
    thick = fields.Char('Thick')
    heat_id = fields.Many2one('heat.heat', 'Heat')


class Heat(models.Model):
    _name = 'heat.heat'
    _description = "Heats"

    @api.onchange('grade_id')
    def _onchange_grade_id(self):
        data = []
        line_ids = []
        # First check if the record is being created or grade_id value if being changed
        if self._context.get('onchange', False):
            # This means the grade_id field value is being changed
            if self.grade_id:
                line_ids = self.grade_id and self.grade_id.line_ids or []
        for i in line_ids:
            data.append((0, 0, {'element_id': i.element_id, 'min_val': i.min_val, 'max_val': i.max_val}))
        self.line_ids = data

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        heats = []
        heats = self.search([('furnace_heat_no', 'ilike', name)])
        res = super(Heat, self).name_search(name, args, operator, limit)
        return list(set(res + (heats and heats.name_get() or [])))

    def name_get(self):
        result = []
        for record in self:
            name = '[' + str(record.furnace_heat_no or "") + ']' + ' ' + record.name
            result.append((record.id, name))
        return result

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('heat.heat') or _('New')
        result = super(Heat, self).create(vals)
        return result

    name = fields.Char('SSAI Heat No.', default='New Heat', required=True)
    furnace_heat_no = fields.Char('Supplier Heat No.', required=True)
    grinding = fields.Boolean('Grinding')
    date = fields.Char('Date Rcvd', required=True, default=fields.Date.today())
    truck_no = fields.Char('Truck No.')
    partner_id = fields.Many2one('res.partner',string=" Supplier")
    stock_picking_id = fields.Many2one('stock.picking', 'Stock Picking')
    source_document = fields.Char(string="Source Doc.", store=True, related='stock_picking_id.origin')
    grade_id = fields.Many2one('material.grade','Material Grade')
    line_ids = fields.One2many('composition.line', 'heat_id', 'Chemical Composition Report')
    surface_inspection = fields.Boolean('Surface Inspection')
    xrf_tested = fields.Boolean('XRF Tested')
    state = fields.Selection(
        [('ok', 'OK'), ('non_confirmance', 'Non Confirmance'), ('rejected', 'Rejected'), ('resolved', 'Resolved')],
        default='ok', string="State")
    remarks = fields.Text('Remarks')
    size = fields.Many2one('ingot.size', 'Size')
    inclusion_rating_ids = fields.One2many('inclusion.rating.line', 'heat_id', 'Inclusion Rating')
    supervisor_id = fields.Many2one('res.users', 'Supervisor', default=lambda self: self.env.user)
    roll_size = fields.Many2many('product.product', string="Rolling Size", help="Rolling Size")
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env['res.company']._company_default_get('sale.order'))
