# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # --- KPI propio "Vendidas" (movimientos de salida DONE) ---
    sold_qty = fields.Float(
        string="Vendidas",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    def _compute_sold_qty(self):
        Move = self.env["stock.move"]

        # Campos disponibles en esta build
        move_fields = Move.fields_get()
        # Para read_group usamos un campo sumable y almacenado
        measure_rg = (
            "product_uom_qty" if "product_uom_qty" in move_fields
            else ("quantity_done" if "quantity_done" in move_fields else None)
        )
        # Fallback para suma manual cuando no hay campo agregable
        measure_fallback = "quantity" if "quantity" in move_fields else None

        # Variantes de todas las plantillas (cálculo vectorizado)
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for tmpl in self:
                tmpl.sold_qty = 0.0
            return

        domain = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]

        qty_by_product = {}

        if measure_rg:
            # Ruta rápida y agregable
            rows = Move.read_group(domain, ["product_id", f"{measure_rg}:sum"], ["product_id"])
            qty_by_product = {
                r["product_id"][0]: r.get(f"{measure_rg}_sum", 0.0) or 0.0
                for r in rows
            }
        elif measure_fallback:
            # Fallback: sumar manualmente 'quantity'
            for r in Move.search(domain).read(["product_id", measure_fallback]):
                pid = r["product_id"][0]
                qty_by_product[pid] = qty_by_product.get(pid, 0.0) + (r.get(measure_fallback) or 0.0)
        else:
            # No hay nada que sumar, dejamos 0.0
            qty_by_product = {}

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
                ("company_id", "=", self.env.company.id),
                ("location_id.usage", "=", "internal"),
                ("location_dest_id.usage", "=", "customer"),
                ("product_id", "in", self.product_variant_ids.ids),
            ],
            "context": {},
        }

    # --- MÉTODO 2: Ajuste del KPI nativo "Vendido" (sales_count) ---
    @api.depends_context("company")
    def _compute_sales_count(self):
        """
        Mantiene el cálculo estándar (líneas de venta) y ADEMÁS suma
        entregas reales (stock.move DONE internal->customer) para cubrir
        ventas por factura directa (sin SO). Evita doble conteo.
        """
        # 1) Comportamiento estándar de Odoo
        super()._compute_sales_count()

        Move = self.env["stock.move"]
        move_fields = Move.fields_get()

        # Igual que arriba: preferimos campo sumable, si no, fallback a suma manual
        measure_rg = (
            "product_uom_qty" if "product_uom_qty" in move_fields
            else ("quantity_done" if "quantity_done" in move_fields else None)
        )
        measure_fallback = "quantity" if "quantity" in move_fields else None

        has_sale_line = "sale_line_id" in move_fields
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            return

        domain = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]
        if has_sale_line:
            # si existe sale_line_id, no contamos movimientos que ya vienen de SO
            domain.append(("sale_line_id", "=", False))

        qty_by_product = {}
        if measure_rg:
            rows = Move.read_group(domain, ["product_id", f"{measure_rg}:sum"], ["product_id"])
            qty_by_product = {
                r["product_id"][0]: r.get(f"{measure_rg}_sum", 0.0) or 0.0
                for r in rows
            }
        elif measure_fallback:
            for r in Move.search(domain).read(["product_id", measure_fallback]):
                pid = r["product_id"][0]
                qty_by_product[pid] = qty_by_product.get(pid, 0.0) + (r.get(measure_fallback) or 0.0)
        else:
            qty_by_product = {}

        for tmpl in self:
            add = 0.0
            for p in tmpl.product_variant_ids:
                add += qty_by_product.get(p.id, 0.0)
            tmpl.sales_count = (tmpl.sales_count or 0.0) + add
