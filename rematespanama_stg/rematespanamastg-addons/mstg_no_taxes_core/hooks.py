# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def _su_env(arg0):
    """Devuelve un Environment con SUPERUSER_ID tanto si nos pasan env como si nos pasan cr."""
    # Caso: nos pasan un Environment
    if hasattr(arg0, "cr") and hasattr(arg0, "uid"):
        cr = arg0.cr
        ctx = getattr(arg0, "context", {}) or {}
        return api.Environment(cr, SUPERUSER_ID, ctx)
    # Caso: nos pasan cursor (cr)
    return api.Environment(arg0, SUPERUSER_ID, {})

def _cleanup(env):
    # 1) Productos: sin impuestos
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
    })
    # 2) Compañías: limpiar impuestos por defecto si esos campos existen
    Company = env["res.company"]
    vals = {}
    for f in ("account_sale_tax_id", "account_purchase_tax_id"):
        if f in Company._fields:
            vals[f] = False
    if vals:
        Company.search([]).write(vals)

def post_init_hook(*args, **kwargs):
    if not args:
        return
    env = _su_env(args[0])      # compatible con post_init_hook(env) y post_init_hook(cr, registry)
    _cleanup(env)
