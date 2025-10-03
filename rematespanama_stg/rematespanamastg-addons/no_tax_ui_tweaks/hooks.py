# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def _run_cleanup(env):
    """Lógica del hook: forzar 'Bien' y sin impuestos en productos + limpiar
    impuestos por defecto en compañías. Ejecuta con superusuario."""
    env = env.sudo()

    # Productos: sin impuestos y tipo "Bien"
    env["product.template"].search([]).write({
        "taxes_id": [(6, 0, [])],
        "supplier_taxes_id": [(6, 0, [])],
        "detailed_type": "product",
    })

    # Compañías: quitar impuestos por defecto si existen esos campos
    Company = env["res.company"]
    updates = {}
    for f in ("account_sale_tax_id", "account_purchase_tax_id"):
        if f in Company._fields:
            updates[f] = False
    if updates:
        Company.search([]).write(updates)

def post_init_hook(*args, **kwargs):
    """
    Compatible con Odoo que llama:
      - post_init_hook(env)
      - post_init_hook(cr, registry)
    """
    if not args:
        return
    # Caso 1: Odoo pasa env directo
    try:
        from odoo.api import Environment
        if len(args) == 1 and hasattr(args[0], "cr") and hasattr(args[0], "uid"):
            env = args[0]
            _run_cleanup(env)
            return
    except Exception:
        pass

    # Caso 2: Odoo pasa (cr, registry)
    if len(args) >= 2:
        cr = args[0]
        env = api.Environment(cr, SUPERUSER_ID, {})
        _run_cleanup(env)
