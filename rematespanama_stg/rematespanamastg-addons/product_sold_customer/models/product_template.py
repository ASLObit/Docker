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

    def _sum_moves_by_product(self, domain):
        """
        Suma robusta por producto SIN usar read_group (algunas builds
        no agregan correctamente 'quantity'). Preferencias:
        - quantity_done si existe y tiene datos
        - product_uom_qty
        - quantity (fallback)
        """
        Move = self.env["stock.move"]
        move_fields = Move.fields_get()

        # Campos posibles
        has_qty_done = "quantity_done" in move_fields
        has_uom_qty = "product_uom_qty" in move_fields
        has_qty = "quantity" in move_fields

        fields_to_read = ["product_id"]
        # Leemos todos los que existan; luego elegimos qué sumar por cada fila
        if has_qty_done:
            fields_to_read.append("quantity_done")
        if has_uom_qty:
            fields_to_read.append("product_uom_qty")
        if has_qty:
            fields_to_read.append("quantity")

        qty_by_product = {}
        for r in Move.search(domain).read(fields_to_read):
            pid = r["product_id"][0]
            # preferencia: quantity_done > product_uom_qty > quantity
            val = 0.0
            if has_qty_done and r.get("quantity_done") not in (False, None):
                val = r.get("quantity_done") or 0.0
            elif has_uom_qty and r.get("product_uom_qty") not in (False, None):
                val = r.get("product_uom_qty") or 0.0
            elif has_qty:
                val = r.get("quantity") or 0.0
            qty_by_product[pid] = qty_by_product.get(pid, 0.0) + val
        return qty_by_product

    def _compute_sold_qty(self):
        # Variantes de todas las plantillas (cálculo vectorizado)
        all_variant_ids = self.mapped("product_variant_ids").ids
        if not all_variant_ids:
            for tmpl in self:
                tmpl.sold_qty = 0.0
            return

        # Outgoing robusto: internal -> customer, DONE, compañía actual
        domain = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]

        qty_by_product = self._sum_moves_by_product(domain)

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
        # 1) Comportamiento estándar de Odoo (cuenta SO)
        super()._compute_sales_count()

        Move = self.env["stock.move"]
        move_fields = Move.fields_get()
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
            # Si viene de SO, ya lo contó el estándar → evitar doble conteo
            domain.append(("sale_line_id", "=", False))

        qty_by_product = self._sum_moves_by_product(domain)

        for tmpl in self:
            add = 0.0
            for p in tmpl.product_variant_ids:
                add += qty_by_product.get(p.id, 0.0)
            tmpl.sales_count = (tmpl.sales_count or 0.0) + add
