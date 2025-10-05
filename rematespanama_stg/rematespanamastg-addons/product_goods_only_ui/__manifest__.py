# -*- coding: utf-8 -*-
{
    "name": "Product Goods Only UI",
    "version": "18.0.0.4",  # ⬅️ súbelo para forzar upgrade
    "summary": "Oculta Tipo de producto e impuestos; fuerza Bien y sin impuestos.",
    "author": "mstg",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": [
        "views/product_views.xml",   # ⬅️ nueva vista heredada
    ],
    "installable": True,
    "application": False,
}
