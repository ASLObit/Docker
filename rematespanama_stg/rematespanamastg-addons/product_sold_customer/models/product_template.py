# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # --- KPI propio "Vendidas (Mov.)": salidas DONE interno -> cliente ---
    sold_qty = fields.Float(
        string="Vendidas (Mov.)",
        compute="_compute_sold_qty",
        digits="Product Unit of Measure",
        store=False,
    )

    def _compute_sold_qty(self):
        """
        Suma movimientos reales de salida (stock.move) en estado 'done',
        desde ubicaciones de uso 'internal' a 'customer', para todas las
        variantes del producto. Se evita read_group porque en algunos
        despliegues el campo de cantidad no está almacenado.
        """
        Move = self.env["stock.move"]
        move_fields = Move.fields_get()
        has_qty_done = "quantity_done" in move_fields
        has_uom_qty = "product_uom_qty" in move_fields
        has_qty = "quantity" in move_fields

        # Variantes por plantilla y universo de variantes
        variants_by_tmpl = {tmpl.id: tmpl.product_variant_ids.ids for tmpl in self}
        all_variant_ids = [pid for ids in variants_by_tmpl.values() for pid in ids]
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

        fields_to_read = ["product_id"]
        if has_qty_done:
            fields_to_read.append("quantity_done")
        if has_uom_qty:
            fields_to_read.append("product_uom_qty")
        if has_qty:
            fields_to_read.append("quantity")

        qty_by_product = {}
        for r in Move.search(domain).read(fields_to_read):
            pid = r["product_id"][0]
            val = 0.0
            if has_qty_done and r.get("quantity_done") not in (None, False):
                val = r.get("quantity_done") or 0.0
            elif has_uom_qty and r.get("product_uom_qty") not in (None, False):
                val = r.get("product_uom_qty") or 0.0
            elif has_qty:
                val = r.get("quantity") or 0.0
            qty_by_product[pid] = qty_by_product.get(pid, 0.0) + val

        for tmpl in self:
            total = 0.0
            for pid in variants_by_tmpl.get(tmpl.id, []):
                total += qty_by_product.get(pid, 0.0)
            tmpl.sold_qty = total

    def action_open_sold_moves(self):
        """Smart button: abrir movimientos de salida 'done' del producto."""
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
        ventas por factura directa (sin SO). Evita doble conteo usando
        sale_line_id = False cuando existe ese campo.
        """
        # 1) comportamiento estándar de Odoo (SO → sales_count)
        super()._compute_sales_count()

        Move = self.env["stock.move"]
        move_fields = Move.fields_get()

        has_sale_line = "sale_line_id" in move_fields
        has_qty_done = "quantity_done" in move_fields
        has_uom_qty = "product_uom_qty" in move_fields
        has_qty = "quantity" in move_fields

        # Variantes por plantilla y universo de variantes
        variants_by_tmpl = {tmpl.id: tmpl.product_variant_ids.ids for tmpl in self}
        all_variant_ids = [pid for ids in variants_by_tmpl.values() for pid in ids]
        if not all_variant_ids:
            return

        # 2) movimientos reales de salida (hechos) hacia cliente
        domain = [
            ("state", "=", "done"),
            ("company_id", "=", self.env.company.id),
            ("location_id.usage", "=", "internal"),
            ("location_dest_id.usage", "=", "customer"),
            ("product_id", "in", all_variant_ids),
        ]
        # no contar lo que ya proviene de líneas de venta (para no duplicar)
        if has_sale_line:
            domain.append(("sale_line_id", "=", False))

        fields_to_read = ["product_id"]
        if has_qty_done:
            fields_to_read.append("quantity_done")
        if has_uom_qty:
            fields_to_read.append("product_uom_qty")
        if has_qty:
            fields_to_read.append("quantity")

        qty_by_product = {}
        for r in Move.search(domain).read(fields_to_read):
            pid = r["product_id"][0]
            val = 0.0
            if has_qty_done and r.get("quantity_done") not in (None, False):
                val = r.get("quantity_done") or 0.0
            elif has_uom_qty and r.get("product_uom_qty") not in (None, False):
                val = r.get("product_uom_qty") or 0.0
            elif has_qty:
                val = r.get("quantity") or 0.0
            qty_by_product[pid] = qty_by_product.get(pid, 0.0) + val

        # 3) sumar a cada plantilla sin duplicar lo ya calculado por Odoo
        for tmpl in self:
            add = 0.0
            for pid in variants_by_tmpl.get(tmpl.id, []):
                add += qty_by_product.get(pid, 0.0)
            tmpl.sales_count = (tmpl.sales_count or 0.0) + add
