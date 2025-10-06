# coding: utf-8
from odoo import api, SUPERUSER_ID

def _ensure_env(*args, **kwargs):
    """
    Devuelve un Environment con superusuario (sudo) a partir de:
      - env (instancia real)
      - (cr, registry)
      - objetos que traigan .cr
    """
    if args:
        a0 = args[0]
        # Caso: env real
        if hasattr(a0, "sudo") and hasattr(a0, "cr"):
            try:
                return a0.sudo()
            except Exception:
                pass
        # Caso: trae .cr (env-like)
        cr = getattr(a0, "cr", None)
        if cr is not None:
            return api.Environment(cr, SUPERUSER_ID, {})
        # Caso: cursor directo (duck-typing)
        if hasattr(a0, "execute"):
            return api.Environment(a0, SUPERUSER_ID, {})
    # Último intento: kwargs con cr
    cr = kwargs.get("cr")
    if cr is not None:
        return api.Environment(cr, SUPERUSER_ID, {})
    raise ValueError("currency_no_decimals: no se pudo construir un Environment en post_init_hook")

def post_init_hook(*args, **kwargs):
    env = _ensure_env(*args, **kwargs)
    # Forzar sin decimales a las monedas usadas por las compañías
    companies = env["res.company"].search([])
    currencies = companies.mapped("currency_id")
    if currencies:
        # rounding=1.0 => decimal_places = 0
        currencies.write({"rounding": 1.0})
