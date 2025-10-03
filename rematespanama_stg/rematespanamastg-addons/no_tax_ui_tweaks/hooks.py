# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """Deja todo sin impuestos y sin impuestos por defecto de compañía."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Quitar impuestos de TODOS los productos existentes
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
        "detailed_type": "product",
    })
    # Limpiar impuestos por defecto de compañía (si existen en este build)
    Company = env["res.company"]
    fields_to_clear = []
    for name in ("account_sale_tax_id", "account_purchase_tax_id"):
        if name in Company._fields:
            fields_to_clear.append(name)
    if fields_to_clear:
        Company.search([]).write({f: False for f in fields_to_clear})
