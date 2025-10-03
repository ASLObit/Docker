# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    # --- KPI propio "Vendidas" (solo para botón debug opcional; no toca el nativo) ---
    sold_qty = fields.Float(
        string="Vendidas (mov.)",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    def _compute_sold_qty(self):
        Move = self.env["stock.move"]
        mf = Move.fields_get()
        qty_key = (
            "quantity_done" if "quantity_done" in mf
            else ("quantity" if "quantity" in mf else "product_uom_qty")
        )

        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for t in self:
                t.sold_qty = 0.0
            return

        dom = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]

        # Sumar a mano (sin read_group para evitar problemas de agregación)
        qty_by_product = {}
        for r in Move.search(dom).read(["product_id", qty_key]):
            pid = r["product_id"][0]
            qty_by_product[pid] = qty_by_product.get(pid, 0.0) + (r.get(qty_key) or 0.0)

        for t in self:
            total = 0.0
            for p in t.product_variant_ids:
                total += qty_by_product.get(p.id, 0.0)
            t.sold_qty = total

    def action_open_sold_moves(self):
        """Abrir movimientos de salida DONE del producto (todas sus variantes)."""
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

    # --- Ajuste del KPI nativo "Vendido" (sales_count) ---
    # Suma el estándar (desde SO) + salidas reales sin SO (factura -> picking).
    @api.depends_context("company")
    def _compute_sales_count(self):
        # 1) Dejar que Odoo calcule lo estándar (líneas de venta / SO)
        super()._compute_sales_count()

        Move = self.env["stock.move"]
        mf = Move.fields_get()
        qty_key = (
            "quantity_done" if "quantity_done" in mf
            else ("quantity" if "quantity" in mf else "product_uom_qty")
        )
        has_sale_line = "sale_line_id" in mf

        # Guardar el valor base que deja Odoo
        base_by_tmpl = {t.id: float(t.sales_count or 0.0) for t in self}

        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            # Si no hay variantes, simplemente re-asignamos el base
            for t in self:
                t.sales_count = base_by_tmpl[t.id]
            return

        dom = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]

        # 2) Sumar solo lo que NO viene de SO para evitar doble conteo
        qty_extra_by_product = {}
        fields_to_read = ["product_id", qty_key]
        if has_sale_line:
            fields_to_read.append("sale_line_id")

        for r in Move.search(dom).read(fields_to_read):
            if has_sale_line and r.get("sale_line_id"):
                # Este movimiento ya fue contado por el cálculo estándar
                continue
            pid = r["product_id"][0]
            qty_extra_by_product[pid] = qty_extra_by_product.get(pid, 0.0) + (r.get(qty_key) or 0.0)

        # 3) Asignar: base + extra_por_movimientos
        for t in self:
            extra = 0.0
            for p in t.product_variant_ids:
                extra += qty_extra_by_product.get(p.id, 0.0)
            t.sales_count = base_by_tmpl[t.id] + extra
