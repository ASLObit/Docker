# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """Al instalar/actualizar:
    - Quita impuestos de todos los productos
    - Borra impuestos por defecto de la compañía (ventas/compras) si existen
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Quitar impuestos en productos existentes
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
    })
    # Borrar impuestos por defecto de compañías (nombres pueden variar por versión)
    Company = env["res.company"]
    fields_to_clear = []
    for name in ("account_sale_tax_id", "account_purchase_tax_id"):
        if name in Company._fields:
            fields_to_clear.append(name)
    if fields_to_clear:
        vals = {f: False for f in fields_to_clear}
        Company.search([]).write(vals)
