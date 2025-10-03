# -*- coding: utf-8 -*-
from odoo import api, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_taxes(self):
        # Forzar SIN impuestos en cualquier línea contable de factura
        return self.env["account.tax"]

    @api.model_create_multi
    def create(self, vals_list):
        for v in vals_list:
            # Quita impuestos que vengan en la creación
            v["tax_ids"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        new_vals = vals.copy()
        if "tax_ids" in new_vals:
            new_vals["tax_ids"] = [(6, 0, [])]
        return super().write(new_vals)
