# -*- coding: utf-8 -*-
from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        for v in vals_list:
            v.setdefault("detailed_type", "product")
            v["taxes_id"] = [(6, 0, [])]
            v["supplier_taxes_id"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        vals = vals.copy()
        if "detailed_type" in vals:
            vals["detailed_type"] = "product"
        if "taxes_id" in vals:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in vals:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        return super().write(vals)
