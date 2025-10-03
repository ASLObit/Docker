# -*- coding: utf-8 -*-
from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        # Siempre como "Bien" y sin impuestos
        for vals in vals_list:
            vals.setdefault("detailed_type", "product")
            vals["taxes_id"] = [(6, 0, [])]
            vals["supplier_taxes_id"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        # Blindaje: aunque intenten cambiar
        force = vals.copy()
        if "detailed_type" in force:
            force["detailed_type"] = "product"
        if "taxes_id" in force:
            force["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in force:
            force["supplier_taxes_id"] = [(6, 0, [])]
        return super().write(force)
