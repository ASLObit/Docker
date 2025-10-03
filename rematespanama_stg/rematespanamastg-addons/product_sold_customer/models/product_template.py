# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # (Opcional) KPI auxiliar por movimientos, ya no lo mostramos en UI,
    # pero lo dejamos por si lo quieres usar en algún debug futuro.
    sold_qty = fields.Float(
        string="Vendidas (mov.)",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    # ---------- Utilidades internas ----------

    def _sum_done_out_moves(self, variant_ids, exclude_from_so):
        """
        Suma cantidades de stock.move en estado DONE, de interno->cliente,
        para las variantes dadas. Si exclude_from_so=True, excluye movimientos
        que tengan sale_line_id (evita doble conteo con lo que ya suma Odoo).
        Devuelve: dict {product_id: qty_sum}
        """
        Move = self.env["stock.move"]
        move_fields = Move.fields_get()

        # Campo de cantidad confiable (orden de preferencia)
        qty_key = (
            "quantity_done" if "quantity_done" in move_fields
            else "quantity" if "quantity" in move_fields
            else "product_uom_qty"
        )

        fields_to_read = ["product_id", qty_key]

        dom = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", variant_ids),
        ]
        if exclude_from_so and "sale_line_id" in move_fields:
            dom.append(("sale_line_id", "=", False))

        qty_by_product = {}
        for r in Move.search(dom).read(fields_to_read):
            pid = r["product_id"][0]
            val = r.get(qty_key) or 0.0
            qty_by_product[pid] = qty_by_product.get(pid, 0.0) + val
        return qty_by_product

    # ---------- KPI auxiliar por movimientos (no visible) ----------

    def _compute_sold_qty(self):
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for tmpl in self:
                tmpl.sold_qty = 0.0
            return

        # Aquí contamos TODO movimiento done interno->cliente (venga o no de SO)
        qty_by_product = self._sum_done_out_moves(
            all_variant_ids, exclude_from_so=False
        )

        for tmpl in self:
            total = 0.0
            for p in tmpl.product_variant_ids:
                total += qty_by_product.get(p.id, 0.0)
            tmpl.sold_qty = total

    # ---------- Ajuste del KPI nativo "Vendido" (sales_count) ----------

    @api.depends_context("company")
    def _compute_sales_count(self):
        """
        1) Ejecuta el cómputo estándar (líneas de venta de SO).
        2) Suma ENTREGAS reales (stock.move DONE interno->cliente) que NO provienen de SO
           para cubrir ventas que hiciste por factura directa. Evita doble conteo.
        """
        # 1) core de Odoo (cuenta lo que viene de pedidos de venta)
        super()._compute_sales_count()

        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            return

        # 2) añade movimientos de factura (sin sale_line_id)
        extra_by_product = self._sum_done_out_moves(
            all_variant_ids, exclude_from_so=True
        )

        for tmpl in self:
            add = 0.0
            for p in tmpl.product_variant_ids:
                add += extra_by_product.get(p.id, 0.0)
            tmpl.sales_count = (tmpl.sales_count or 0.0) + add

    # (Opcional) Acción para abrir los movimientos; ya no hay botón en la vista,
    # pero puedes llamarla desde una acción de servidor si la necesitas.
    def action_open_sold_moves(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Ventas (Movimientos)"),
            "res_model": "stock.move",
            "view_mode": "tree,form",
            "target": "current",
            "domain": [
                ("state", "=", "done"),
                ("company_id", "=", self.env.company.id),
                ("location_id.usage", "=", "internal"),
                ("location_dest_id.usage", "=", "customer"),
                ("product_id", "in", self.product_variant_ids.ids),
            ],
            "context": {},
        }
