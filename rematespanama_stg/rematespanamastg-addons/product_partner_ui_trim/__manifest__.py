# -*- coding: utf-8 -*-
{
    "name": "UI Trim: Product & Partner",
    "version": "18.0.0.1",
    "summary": "Oculta pestañas/estadísticos en productos y campos en clientes",
    "author": "asloos",
    "depends": ["base", "product", "stock", "contacts"],
    "data": [
        "views/product_views.xml",
        "views/res_partner_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_partner_ui_trim/static/src/css/hide_stats.css",
        ],
    },
    "installable": True,
    "application": False,
}
