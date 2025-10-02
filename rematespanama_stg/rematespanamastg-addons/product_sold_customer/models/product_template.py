from odoo import api, fields, models

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
            else "product_uom_qty"  # fallback seguro
        )

        # Obtener todos los product.product (variantes) de las plantillas en lote
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
        # Agrupar por product_id y sumar la medida
        rows = Move.read_group(
            domain,
            ["product_id", f"{measure}:sum"],
            ["product_id"],
        )
        qty_by_product = {
            r["product_id"][0]: r[f"{measure}_sum"] for r in rows
        }

        for tmpl in self:
            total = 0.0
            for p in tmpl.product_variant_ids:
                total += qty_by_product.get(p.id, 0.0)
            tmpl.sold_qty = total
