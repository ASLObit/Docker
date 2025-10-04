# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def _run_cleanup(env):
    """Forzar 'Bien' y sin impuestos en productos + limpiar impuestos por defecto en compañías."""
    env = env.sudo()

    # Productos: sin impuestos y tipo "Bien"
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
        "detailed_type": "product",
    })

    # Compañías: quitar impuestos por defecto si esos campos existen
    Company = env["res.company"]
    vals = {}
    for f in ("account_sale_tax_id", "account_purchase_tax_id"):
        if f in Company._fields:
            vals[f] = False
    if vals:
        Company.search([]).write(vals)

def post_init_hook(*args, **_kwargs):
    """
    Compatible con Odoo que llama:
      - post_init_hook(env)
      - post_init_hook(cr, registry)
    """
    if not args:
        return

    first = args[0]
    # Caso 1: nos pasan un Environment (env)
    if hasattr(first, "cr") and hasattr(first, "uid"):
        _run_cleanup(first)
        return

    # Caso 2: nos pasan (cr, registry)
    if len(args) >= 2:
        cr = first
        env = api.Environment(cr, SUPERUSER_ID, {})
        _run_cleanup(env)
