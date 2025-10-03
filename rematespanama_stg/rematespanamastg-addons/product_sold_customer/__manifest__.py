{
    "name": "Product Sold To Customer (no Sales)",
    "summary": "Muestra unidades entregadas a cliente desde movimientos de stock",
    "version": "18.0.3.0.9",
    "license": "LGPL-3",
    "author": "Tu Equipo",
    "depends": ["stock"],
    "data": [
        "views/product_views.xml",
    ],
    "application": False,
    "installable": True,
}

{
    "name": "Product Sold on Customer Moves",
    "version": "18.0.3.0.10",
    "depends": [
        "product",
        "stock",
        "sale",
        "sale_stock",
    ],
    "data": [
    ],
    "installable": True,
}
