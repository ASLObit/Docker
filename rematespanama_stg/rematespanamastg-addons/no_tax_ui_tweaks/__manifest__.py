# -*- coding: utf-8 -*-
{
    "name": "No Taxes + UI Tweaks (Remates Panamá)",
    "version": "18.0.0.1",
    "author": "ASLObit",
    "license": "LGPL-3",
    "depends": ["base", "product", "account", "contacts"],
    "data": [
        "views/product_views.xml",
        "views/account_move_views.xml",
        "views/res_partner_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "application": False,
    "installable": True,
}
