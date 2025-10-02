# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

# Computa "Vendidas" sobre stock.move (salidas a cliente en estado done)
# y abre los movimientos desde un smart button (action_open_sold_moves).

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sold_qty = fields.Float(
        string="Vendidas",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    def _compute_sold_qty(self):
        Move = self.env["stock.move"]
        # Detectar el campo de cantidad disponible en esta build
        move_fields = Move.fields_get()
        measure = (
            "quantity" if "quantity" in move_fields
            else "quantity_done" if "quantity_done" in move_fields
            else "product_uom_qty"  # fallback seguro
        )

        # Variantes de todas las plantillas a la vez (mejor rendimiento)
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for tmpl in self:
                tmpl.sold_qty = 0.0
            return

        domain = [
            ("state", "=", "done"),
            ("picking_code", "=", "outgoing"),   # salidas
            ("product_id", "in", all_variant_ids),
        ]

        rows = Move.read_group(
            domain,
            ["product_id", f"{measure}:sum"],
            ["product_id"],
        )
        qty_by_product = {
            r["product_id"][0]: r.get(f"{measure}_sum", 0.0) for r in rows
        }

        for tmpl in self:
            total = 0.0
            for p in tmpl.product_variant_ids:
                total += qty_by_product.get(p.id, 0.0)
            tmpl.sold_qty = total

    def action_open_sold_moves(self):
        """Abrir movimientos de salida 'done' del producto (cualquier variante)."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Ventas (Movimientos)"),
            "res_model": "stock.move",
            "view_mode": "tree,form",
            "target": "current",
            "domain": [
                ("state", "=", "done"),
                ("picking_code", "=", "outgoing"),
                ("product_id", "in", self.product_variant_ids.ids),
            ],
            "context": {},
        }
