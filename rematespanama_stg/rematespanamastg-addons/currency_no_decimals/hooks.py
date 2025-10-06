# coding: utf-8
from odoo import api, SUPERUSER_ID

def _apply_no_decimals(env):
    """Forzar que las monedas usadas por las compañías no tengan decimales."""
    env = env.sudo()
    companies = env['res.company'].search([])
    currencies = companies.mapped('currency_id')
    if currencies:
        # rounding=1.0  => decimal_places = 0 (sin decimales)
        currencies.write({'rounding': 1.0})

def post_init_hook(*args, **kwargs):
    """
    Soporta ambas llamadas:
      - v16: post_init_hook(cr, registry)
      - v17/v18: post_init_hook(env)
    """
    if len(args) >= 2:
        # Caso (cr, registry)
        cr = args[0]
        env = api.Environment(cr, SUPERUSER_ID, {})
    else:
        # Caso (env) directo
        env = args[0]
        # Si por alguna razón no es un Environment, lo reconstruimos
        if not hasattr(env, 'cr'):
            cr = getattr(env, 'cr', None) or kwargs.get('cr')
            env = api.Environment(cr, SUPERUSER_ID, {})
    _apply_no_decimals(env)
