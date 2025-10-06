# models/product.py
from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Forzar Bien solo usando detailed_type
            vals.setdefault('detailed_type', 'product')
            # dejar sin impuestos por defecto
            vals.setdefault('taxes_id', [(6, 0, [])])
            vals.setdefault('supplier_taxes_id', [(6, 0, [])])
        return super().create(vals_list)

    def write(self, vals):
        # Si no se está cambiando el tipo, asegurarlo como 'product'
        if 'detailed_type' not in vals:
            vals = dict(vals, detailed_type='product')
        # Mantener sin impuestos si no se pasan explícitamente
        if 'taxes_id' not in vals:
            vals = dict(vals, taxes_id=[(6, 0, [])])
        if 'supplier_taxes_id' not in vals:
            vals = dict(vals, supplier_taxes_id=[(6, 0, [])])
        return super().write(vals)
# models/product.py
from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Forzar Bien solo usando detailed_type
            vals.setdefault('detailed_type', 'product')
            # dejar sin impuestos por defecto
            vals.setdefault('taxes_id', [(6, 0, [])])
            vals.setdefault('supplier_taxes_id', [(6, 0, [])])
        return super().create(vals_list)

    def write(self, vals):
        # Si no se está cambiando el tipo, asegurarlo como 'product'
        if 'detailed_type' not in vals:
            vals = dict(vals, detailed_type='product')
        # Mantener sin impuestos si no se pasan explícitamente
        if 'taxes_id' not in vals:
            vals = dict(vals, taxes_id=[(6, 0, [])])
        if 'supplier_taxes_id' not in vals:
            vals = dict(vals, supplier_taxes_id=[(6, 0, [])])
        return super().write(vals)
