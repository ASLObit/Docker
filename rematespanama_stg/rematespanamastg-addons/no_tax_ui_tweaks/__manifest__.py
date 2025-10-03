# -*- coding: utf-8 -*-
{
    "name": "No Taxes + UI Tweaks (Remates Panamá)",
    "version": "18.0.0.4",  # <— subido
    "author": "ASLObit",
    "license": "LGPL-3",
    "depends": ["base", "web", "product", "account", "contacts"],
    "data": [
        "views/assets.xml",            # <— nuevo formato ir.asset
        "views/res_partner_views.xml", # Contacto -> Dirección y ocultar campos
    ],
    "post_init_hook": "post_init_hook",
    "application": False,
    "installable": True,
}
