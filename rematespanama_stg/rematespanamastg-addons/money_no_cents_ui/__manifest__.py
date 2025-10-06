# coding: utf-8
{
    "name": "Money No Cents (UI only)",
    "version": "18.0.1.1",  # ⬅️ súbela para forzar actualización
    "summary": "Muestra importes monetarios sin decimales en la interfaz",
    "category": "Tools",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "money_no_cents_ui/static/src/js/monetary_no_cents.js",
        ],
        "web.assets_frontend": [
            "money_no_cents_ui/static/src/js/monetary_no_cents.js",
        ],
    },
    "license": "LGPL-3",
}
