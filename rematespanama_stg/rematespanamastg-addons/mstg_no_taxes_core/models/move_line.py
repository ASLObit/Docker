# -*- coding: utf-8 -*-
from odoo import models, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("product_id")
    def _onchange_clear_taxes(self):
        # Solo en líneas de factura/recibo (no en asientos contables genéricos)
        if self.move_id and self.move_id.is_invoice(include_receipts=True):
            self.tax_ids = [(6, 0, [])]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Blindaje: ninguna línea de factura con impuestos
            vals["tax_ids"] = [(6, 0, [])]
        return super().create(vals_list)

    def write(self, vals):
        if "tax_ids" in vals:
            vals["tax_ids"] = [(6, 0, [])]
        return super().write(vals)
