from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        # Ejecuta primero el método original
        res = super().action_post()

        for move in self:
            if move.move_type == 'out_invoice':  # Solo facturas de cliente
                picking_type = self.env.ref('stock.picking_type_out')  # Operación salida
                picking = self.env['stock.picking'].create({
                    'partner_id': move.partner_id.id,
                    'picking_type_id': picking_type.id,
                    'origin': move.name,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': move.partner_id.property_stock_customer.id,
                })

                for line in move.invoice_line_ids.filtered(lambda l: l.product_id.type == 'product'):
                    self.env['stock.move'].create({
                        'picking_id': picking.id,
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.product_uom_id.id,
                        'location_id': picking.location_id.id,
                        'location_dest_id': picking.location_dest_id.id,
                    })

                # Confirmar y validar el picking
                picking.action_confirm()
                picking.action_assign()
                picking.button_validate()

        return res