# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

# Precisiones que quieres a 0 dígitos
DP_TO_ZERO = [
    "Product Price",
    "Discount",
    "Product Unit of Measure",
    "Volume",
]

def _apply_precisions(env):
    dp = env['decimal.precision']
    recs = dp.search([('name', 'in', DP_TO_ZERO)])
    if recs:
        recs.write({'digits': 0})

def post_init_hook(*args, **kwargs):
    """
    Compatible con:
      - Odoo 18+: post_init_hook(env)
      - Odoo antiguas: post_init_hook(cr, registry)
    """
    first = args[0] if args else None
    # Si es un Environment (tiene cr y uid), úsalo tal cual
    if first is not None and hasattr(first, 'cr') and hasattr(first, 'uid'):
        env = first
    else:
        # Forma (cr, registry)
        cr = first
        env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_precisions(env)
