#    Author: Guewen Baconnier
#    Copyright 2013 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import except_orm
from odoo.tools.translate import _

class Element(models.Model):
    _name = "element.element"
    _description = "Chemical Element"

    name = fields.Char('Name',required=True)
    code = fields.Char('Code',required=True)


class CompositionLine(models.Model):
    _name = "composition.line"
    _description = "Composition Line"

    element_id = fields.Many2one('element.element', 'Element', required=True)
    min_val = fields.Char('Min')
    max_val = fields.Char('Max')
    actual_val = fields.Char('Actual')
    furnace_val = fields.Char('Furnace Report')
    grade_id = fields.Many2one('material.grade', 'Material Grade')
    sequence = fields.Integer('Sequence')


class MaterialGrade(models.Model):
    _name = 'material.grade'
    _description = "Material Grade"

    _sql_constraints = [
        ('grade_name_uniq', 'unique(name)', 'Grade name should be unique!'),
    ]

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean('Active', default=True)
    remarks = fields.Text('Remarks')
    name_str = fields.Char('Print Name')
    line_ids = fields.One2many('composition.line','grade_id','Composition')
