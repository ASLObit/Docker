# coding: utf-8
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """Al instalar: forzar redondeo entero para las monedas de las compañías."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    Company = env["res.company"].sudo()
    for company in Company.search([]):
        currency = company.currency_id
        if currency and currency.rounding != 1.0:
            # rounding=1.0  => decimal_places=0 (sin decimales)
            currency.write({"rounding": 1.0})
