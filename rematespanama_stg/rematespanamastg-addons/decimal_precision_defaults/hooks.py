# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

DP_NAMES_0 = [
    "Product Price",
    "Discount",
    "Product Unit of Measure",
    "Volume",
]

def _apply_precisions(env):
    # Fuerza a 0 dígitos las precisiones seleccionadas (si existen)
    dp = env['decimal.precision']
    dp.search([('name', 'in', DP_NAMES_0)]).write({'digits': 0})

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_precisions(env)
