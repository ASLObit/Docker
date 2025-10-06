# models/product.py
from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault('detailed_type', 'product')
            vals.setdefault('taxes_id', [(6, 0, [])])
            vals.setdefault('supplier_taxes_id', [(6, 0, [])])
        return super().create(vals_list)

    def write(self, vals):
        if 'detailed_type' not in vals:
            vals = dict(vals, detailed_type='product')
        if 'taxes_id' not in vals:
            vals = dict(vals, taxes_id=[(6, 0, [])])
        if 'supplier_taxes_id' not in vals:
            vals = dict(vals, supplier_taxes_id=[(6, 0, [])])
        return super().write(vals)
