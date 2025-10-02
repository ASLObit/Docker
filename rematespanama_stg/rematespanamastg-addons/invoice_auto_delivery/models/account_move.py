# -*- coding: utf-8 -*-
from odoo import api, models, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        for inv in self.filtered(lambda m: m.move_type == "out_invoice" and m.state == "posted"):
            try:
                inv._auto_create_delivery_from_invoice()
            except Exception as e:
                # no rompemos el posteo de la factura; dejamos traza en el chatter
                inv.message_post(body=f"Auto Stock ERROR: {e}")
        return res

    def _auto_create_delivery_from_invoice(self):
        self.ensure_one()
        SP = self.env["stock.picking"]
        SM = self.env["stock.move"]
        WH = self.env["stock.warehouse"]

        # 1) Almacén por compañía
        wh = WH.search([("company_id", "=", self.company_id.id)], limit=1)
        if not wh:
            self.message_post(body=_("Auto Stock: No warehouse found for company"))
            return

        src = wh.lot_stock_id
        dest = self.partner_id.property_stock_customer

        # 2) Líneas válidas (ni cabeceras/notas, qty>0, producto almacenable/consumible)
        def _ptype(prod):
            # tolerante: revisa en product.product y en la template
            return (
                getattr(prod, "detailed_type", None)
                or getattr(prod.product_tmpl_id, "detailed_type", None)
                or getattr(prod, "type", None)
                or getattr(prod.product_tmpl_id, "type", "product")
            )

        valid = self.invoice_line_ids.filtered(
            lambda l: l.product_id
            and (_ptype(l.product_id) in ("product", "consu"))
            and (not l.display_type or l.display_type == "product")
            and float(l.quantity or 0.0) > 0.0
        )
        if not valid:
            self.message_post(body=_("Auto Stock: no stockable product lines (revise tipo/cantidad)"))
            return

        # 3) Picking
        picking = SP.create({
            "partner_id":       self.partner_id.id,
            "picking_type_id":  wh.out_type_id.id,
            "location_id":      src.id,
            "location_dest_id": dest.id,
            "origin":           self.name,
            "move_type":        "direct",
            "company_id":       self.company_id.id,
        })

        # 4) Movimientos
        for l in valid:
            SM.create({
                "name":            l.name or l.product_id.display_name,
                "product_id":      l.product_id.id,
                "product_uom":     l.product_uom_id.id,
                "product_uom_qty": float(l.quantity),
                "picking_id":      picking.id,
                "location_id":     src.id,
                "location_dest_id": dest.id,
                "company_id":      self.company_id.id,
            })

        # 5) Confirmar, reservar y validar (resuelve wizards)
        picking.action_confirm()
        picking.action_assign()
        res = picking.button_validate()
        if isinstance(res, dict):
            if res.get("res_model") == "stock.immediate.transfer":
                self.env["stock.immediate.transfer"].browse(res["res_id"]).process()
            elif res.get("res_model") == "stock.backorder.confirmation":
                self.env["stock.backorder.confirmation"].browse(res["res_id"]).process()

        self.message_post(body=_("Auto Stock: picking %s confirmado y validado") % picking.name)
