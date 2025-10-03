# -*- coding: utf-8 -*-
from odoo import api, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_taxes(self):
        return self.env["account.tax"]

    @api.model_create_multi
    def create(self, vals_list):
        for v in vals_list:
            v["tax_ids"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        vals = vals.copy()
        if "tax_ids" in vals:
            vals["tax_ids"] = [(6, 0, [])]
        return super().write(vals)
