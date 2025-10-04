# -*- coding: utf-8 -*-
from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        # Fuerza valor inicial de tipo
        if "detailed_type" in self._fields:
            vals["detailed_type"] = "product"
        if "type" in self._fields:
            vals["type"] = "product"
        # Limpia impuestos por si la compañía tuviera defaults
        if "taxes_id" in self._fields:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in self._fields:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Tipo siempre 'product'
            if "detailed_type" in self._fields:
                vals["detailed_type"] = "product"
            if "type" in self._fields:
                vals["type"] = "product"
            # Nunca guardar impuestos en producto
            if "taxes_id" in self._fields:
                vals["taxes_id"] = [(6, 0, [])]
            if "supplier_taxes_id" in self._fields:
                vals["supplier_taxes_id"] = [(6, 0, [])]
        recs = super().create(vals_list)
        # Doble seguro post-create
        for r in recs:
            write_vals = {}
            if "detailed_type" in r._fields and r.detailed_type != "product":
                write_vals["detailed_type"] = "product"
            if "type" in r._fields and getattr(r, "type", None) != "product":
                write_vals["type"] = "product"
            if "taxes_id" in r._fields and r.taxes_id:
                write_vals["taxes_id"] = [(6, 0, [])]
            if "supplier_taxes_id" in r._fields and r.supplier_taxes_id:
                write_vals["supplier_taxes_id"] = [(6, 0, [])]
            if write_vals:
                super(ProductTemplate, r).write(write_vals)
        return recs

    def write(self, vals):
        # Blindaje en edición
        if "detailed_type" in vals:
            vals["detailed_type"] = "product"
        if "type" in vals:
            vals["type"] = "product"
        if "taxes_id" in vals:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in vals:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        res = super().write(vals)
        # Doble seguro post-write
        for r in self:
            fix = {}
            if "detailed_type" in r._fields and r.detailed_type != "product":
                fix["detailed_type"] = "product"
            if "type" in r._fields and getattr(r, "type", None) != "product":
                fix["type"] = "product"
            if "taxes_id" in r._fields and r.taxes_id:
                fix["taxes_id"] = [(6, 0, [])]
            if "supplier_taxes_id" in r._fields and r.supplier_taxes_id:
                fix["supplier_taxes_id"] = [(6, 0, [])]
            if fix:
                super(ProductTemplate, r).write(fix)
        return res
