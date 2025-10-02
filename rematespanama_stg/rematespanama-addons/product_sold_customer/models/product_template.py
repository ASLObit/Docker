from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sold_customer_qty = fields.Float(
        string="Vendidas (entregado)",
        compute="_compute_sold_customer_qty",
        digits="Product Unit of Measure",
        compute_sudo=True,
    )

    def _compute_sold_customer_qty(self):
        for tmpl in self:
            qty = 0.0
            variants = tmpl.product_variant_ids.ids
            if not variants:
                tmpl.sold_customer_qty = 0.0
                continue

            # Movimientos realizados hacia cliente
            domain = [
                ("state", "=", "done"),
                ("product_id", "in", variants),
                ("location_dest_id.usage", "=", "customer"),
            ]
            # Agrupamos por UoM y convertimos a la UoM del template
            groups = self.env["stock.move.line"].read_group(
                domain, ["product_uom_id", "qty_done:sum"], ["product_uom_id"]
            )
            uom = tmpl.uom_id
            for g in groups:
                line_uom = self.env["uom.uom"].browse(g["product_uom_id"][0])
                qty += line_uom._compute_quantity(g["qty_done"], uom, round=False)
            tmpl.sold_customer_qty = qty

    def action_view_sold_move_lines(self):
        self.ensure_one()
        Action = self.env["ir.actions.act_window"]
        action = {
            "name": "Movimientos entregados",
            "type": "ir.actions.act_window",
            "res_model": "stock.move.line",
            "view_mode": "tree,form",
            "domain": [
                ("state", "=", "done"),
                ("product_id", "in", self.product_variant_ids.ids),
                ("location_dest_id.usage", "=", "customer"),
            ],
            "context": {"search_default_groupby_product_id": 1},
            "target": "current",
        }
        return action
