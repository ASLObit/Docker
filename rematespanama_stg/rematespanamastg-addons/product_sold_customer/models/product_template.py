from odoo import api, fields, models, _
# Computa Vendidas sobre stock.move (no move.line) y abre movimientos desde el botón

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
        # Elegir el campo de cantidad que exista en esta build
        move_fields = Move.fields_get()
        measure = (
            "quantity" if "quantity" in move_fields
            else "quantity_done" if "quantity_done" in move_fields
            else "product_uom_qty"
        )

        all_variants = self.mapped("product_variant_ids").ids
        if not all_variants:
            for tmpl in self:
                tmpl.sold_qty = 0.0
            return

        domain = [
            ("state", "=", "done"),
            ("picking_code", "=", "outgoing"),
            ("product_id", "in", all_variants),
        ]
        rows = Move.read_group(
            domain,
            ["product_id", f"{measure}:sum"],
            ["product_id"],
        )
        qty_by_product = {r["product_id"][0]: r[f"{measure}_sum"] for r in rows}

        for tmpl in self:
            total = 0.0
            for p in tmpl.product_variant_ids:
                total += qty_by_product.get(p.id, 0.0)
            tmpl.sold_qty = total

    def action_open_sold_moves(self):
        """Botón del smart button: abrir movimientos de salida 'done' del producto."""
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
