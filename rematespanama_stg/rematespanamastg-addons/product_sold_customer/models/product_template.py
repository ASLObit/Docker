# -*- coding: utf-8 -*-
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # -------------------------------------------------------------------------
    # KPI nativo "Vendido" (sales_count)
    # Recomputamos completamente para incluir:
    #   1) Ventas estándar (líneas de venta)
    #   2) Entregas reales desde facturas: stock.move DONE internal->customer
    #      que NO provienen de sale_line_id (evita doble conteo)
    # -------------------------------------------------------------------------
    @api.depends_context("company")
    def _compute_sales_count(self):
        OrderLine = self.env["sale.order.line"].sudo()
        Move = self.env["stock.move"].sudo()

        # Todas las variantes de TODOS los templates en lote (mejor rendimiento)
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for tmpl in self:
                tmpl.sales_count = 0.0
            return

        # ---------- 1) Base: líneas de venta ----------
        base_rows = OrderLine.read_group(
            [
                ("state", "in", ["sale", "done"]),
                ("company_id", "=", self.env.company.id),
                ("product_id", "in", all_variant_ids),
                ("is_downpayment", "=", False),
            ],
            ["product_id", "product_uom_qty:sum"],
            ["product_id"],
        )
        base_by_product = {
            r["product_id"][0]: r.get("product_uom_qty_sum", 0.0) for r in base_rows
        }

        # ---------- 2) Extra: movimientos reales desde factura ----------
        # Elegimos el campo de cantidad que exista en esta build
        move_fields = Move.fields_get()
        qty_field = (
            "quantity"
            if "quantity" in move_fields
            else ("quantity_done" if "quantity_done" in move_fields else "product_uom_qty")
        )

        # Sumamos manualmente (read_group con "quantity" puede devolver 0)
        extra_by_product = {}
        extra_moves = Move.search(
            [
                ("state", "=", "done"),
                ("company_id", "=", self.env.company.id),
                ("location_id.usage", "=", "internal"),
                ("location_dest_id.usage", "=", "customer"),
                ("product_id", "in", all_variant_ids),
                # evita contar lo que ya viene de una venta
                ("sale_line_id", "=", False),
            ]
        ).read(["product_id", qty_field])

        for r in extra_moves:
            pid = r["product_id"][0]
            qty = r.get(qty_field) or 0.0
            extra_by_product[pid] = extra_by_product.get(pid, 0.0) + qty

        # ---------- Asignar por plantilla ----------
        for tmpl in self:
            total = 0.0
            for p in tmpl.product_variant_ids:
                total += base_by_product.get(p.id, 0.0)
                total += extra_by_product.get(p.id, 0.0)
            tmpl.sales_count = total
