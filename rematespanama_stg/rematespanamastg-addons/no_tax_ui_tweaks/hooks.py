# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """Se ejecuta justo después de instalar el módulo."""
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Productos: sin impuestos y tipo "Bien"
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
        "detailed_type": "product",
    })

    # Compañías: quitar impuestos por defecto (si existen esos campos)
    Company = env["res.company"]
    to_clear = {}
    for f in ("account_sale_tax_id", "account_purchase_tax_id"):
        if f in Company._fields:
            to_clear[f] = False
    if to_clear:
        Company.search([]).write(to_clear)
