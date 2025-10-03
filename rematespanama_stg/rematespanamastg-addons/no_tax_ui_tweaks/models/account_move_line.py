# -*- coding: utf-8 -*-
from odoo import api, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_taxes(self):
        # Nunca calcular impuestos por defecto
        return self.env["account.tax"]

    @api.model_create_multi
    def create(self, vals_list):
        for v in vals_list:
            v["tax_ids"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        force = vals.copy()
        if "tax_ids" in force:
            force["tax_ids"] = [(6, 0, [])]
        return super().write(force)
