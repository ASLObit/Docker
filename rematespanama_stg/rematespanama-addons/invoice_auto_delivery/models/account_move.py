from odoo import api, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        invoices = self.filtered(lambda m: m.move_type == "out_invoice" and m.state == "posted")
        for inv in invoices:
            try:
                inv._auto_create_delivery_from_invoice()
            except Exception as e:
                inv.message_post(body=f"Auto Stock ERROR: {e}")
        return res

    def _auto_create_delivery_from_invoice(self):
        self.ensure_one()
        StockPicking = self.env["stock.picking"]
        StockMove = self.env["stock.move"]
        WH = self.env["stock.warehouse"]

        # 1) Almacén por compañía
        wh = WH.search([("company_id", "=", self.company_id.id)], limit=1)
        if not wh:
            self.message_post(body=_("Auto Stock: No warehouse found for company"))
            return

        src = wh.lot_stock_id
        dest = self.partner_id.property_stock_customer

        # 2) Filtrar líneas válidas (producto/consumible, qty>0, no cabeceras)
        lines = self.invoice_line_ids.filtered(
            lambda l: l.product_id
            and (l.product_id.detailed_type in ("product", "consu"))
            and not l.display_type
            and (l.quantity or 0.0) > 0.0
        )
        if not lines:
            self.message_post(body=_("Auto Stock: no stockable product lines (revise tipo/cantidad)"))
            return

        # 3) Crear picking
        picking = StockPicking.create({
            "partner_id": self.partner_id.id,
            "picking_type_id": wh.out_type_id.id,
            "location_id": src.id,
            "location_dest_id": dest.id,
            "origin": self.name,
            "move_type": "direct",
            "company_id": self.company_id.id,
        })

        # 4) Movimientos
        for l in lines:
            StockMove.create({
                "name": l.name or l.product_id.display_name,
                "product_id": l.product_id.id,
                "product_uom": l.product_uom_id.id,
                "product_uom_qty": l.quantity,
                "picking_id": picking.id,
                "location_id": src.id,
                "location_dest_id": dest.id,
                "company_id": self.company_id.id,
            })

        # 5) Confirmar, reservar y validar (procesa wizards)
        picking.action_confirm()
        picking.action_assign()
        res = picking.button_validate()
        if isinstance(res, dict):
            if res.get("res_model") == "stock.immediate.transfer":
                self.env["stock.immediate.transfer"].browse(res["res_id"]).process()
            elif res.get("res_model") == "stock.backorder.confirmation":
                self.env["stock.backorder.confirmation"].browse(res["res_id"]).process()

        self.message_post(body=_("Auto Stock: picking %s confirmado y validado") % picking.name)
