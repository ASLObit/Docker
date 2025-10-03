{
    "name": "No Taxes + UI Tweaks (Remates Panamá)",
    "version": "18.0.0.6",  # <- súbela para forzar actualización
    "author": "ASLObit",
    "license": "LGPL-3",
    "depends": ["base", "web", "product", "account", "contacts"],
    "data": [
        "views/assets.xml",
        "views/res_partner_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
