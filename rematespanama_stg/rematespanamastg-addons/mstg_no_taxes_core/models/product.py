# -*- coding: utf-8 -*-
from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        # Quitar impuestos siempre
        for vals in vals_list:
            vals["taxes_id"] = [(6, 0, [])]
            vals["supplier_taxes_id"] = [(6, 0, [])]
        recs = super().create(vals_list)
        # Doble seguro por si algún flujo mete impuestos luego del create()
        recs.write({
            "taxes_id": [(6, 0, [])],
            "supplier_taxes_id": [(6, 0, [])],
        })
        return recs

    def write(self, vals):
        # Blindaje: si intentan establecer impuestos, los vaciamos
        if "taxes_id" in vals:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in vals:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        return super().write(vals)
