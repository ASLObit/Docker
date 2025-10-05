# -*- coding: utf-8 -*-
from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def default_get(self, fields_list):
        vals = super().default_get(fields_list)
        if "detailed_type" in self._fields:
            vals["detailed_type"] = "product"
        if "type" in self._fields:
            vals["type"] = "product"
        if "taxes_id" in self._fields:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in self._fields:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "detailed_type" in self._fields:
                vals["detailed_type"] = "product"
            if "type" in self._fields:
                vals["type"] = "product"
            if "taxes_id" in self._fields:
                vals["taxes_id"] = [(6, 0, [])]
            if "supplier_taxes_id" in self._fields:
                vals["supplier_taxes_id"] = [(6, 0, [])]
        recs = super().create(vals_list)
        for r in recs:
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
        return recs

    def write(self, vals):
        if "detailed_type" in vals:
            vals["detailed_type"] = "product"
        if "type" in vals:
            vals["type"] = "product"
        if "taxes_id" in vals:
            vals["taxes_id"] = [(6, 0, [])]
        if "supplier_taxes_id" in vals:
            vals["supplier_taxes_id"] = [(6, 0, [])]
        res = super().write(vals)
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
