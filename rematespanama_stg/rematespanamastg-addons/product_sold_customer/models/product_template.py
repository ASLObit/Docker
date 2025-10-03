# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


# ======================================================================
# VARIANTE: aquí es donde Odoo computa "Vendido" y luego el template suma
# ======================================================================
class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends_context("company")
    def _compute_sales_count(self):
        # 1) núcleo de Odoo: líneas de SO
        super()._compute_sales_count()

        Move = self.env["stock.move"]
        mf = Move.fields_get()

        # Campo de cantidad confiable (read_group no sirve si no es stored)
        qty_key = (
            "quantity_done" if "quantity_done" in mf
            else "quantity" if "quantity" in mf
            else "product_uom_qty"
        )

        dom_base = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
        ]
        # Evitar doble conteo con lo que ya cuenta Odoo por SO
        if "sale_line_id" in mf:
            dom_base.append(("sale_line_id", "=", False))

        fields_to_read = ["product_id", qty_key]

        # Sumar por variante
        extra_by_id = {}
        moves = Move.search(dom_base + [("product_id", "in", self.ids)])
        for r in moves.read(fields_to_read):
            pid = r["product_id"][0]
            extra_by_id[pid] = extra_by_id.get(pid, 0.0) + (r.get(qty_key) or 0.0)

        for prod in self:
            prod.sales_count = (prod.sales_count or 0.0) + extra_by_id.get(prod.id, 0.0)


# ======================================================================
# TEMPLATE: deja el cómputo estándar (suma las variantes)
# ======================================================================
class ProductTemplate(models.Model):
    _inherit = "product.template"

    # KPI auxiliar por movimientos (no mostrado en la vista)
    sold_qty = fields.Float(
        string="Vendidas (mov.)",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    def _compute_sold_qty(self):
        """Sólo para debug: todas las salidas DONE interno->cliente, sin
        distinguir si vienen de SO o no."""
        Move = self.env["stock.move"]
        mf = Move.fields_get()
        qty_key = (
            "quantity_done" if "quantity_done" in mf
            else "quantity" if "quantity" in mf
            else "product_uom_qty"
        )
        pids = self.mapped("product_variant_ids").ids
        if not pids:
            for t in self:
                t.sold_qty = 0.0
            return
        dom = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", pids),
        ]
        qty_by = {}
        for r in Move.search(dom).read(["product_id", qty_key]):
            pid = r["product_id"][0]
            qty_by[pid] = qty_by.get(pid, 0.0) + (r.get(qty_key) or 0.0)

        for t in self:
            t.sold_qty = sum(qty_by.get(p.id, 0.0) for p in t.product_variant_ids)

    @api.depends_context("company")
    def _compute_sales_count(self):
        # IMPORTANTE: no añadimos nada aquí; el template suma variantes.
        super()._compute_sales_count()
