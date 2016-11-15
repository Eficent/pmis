# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.exceptions import Warning


class StockMove(models.Model):

    _inherit = "stock.move"

    @api.model
    def _add_move_fields(self, move, default_val):
        return default_val

    @api.multi
    def action_scrap(self, quantity, location_id, restrict_lot_id=False, restrict_partner_id=False):
        """ Move the scrap/damaged product into scrap location
        @param cr: the database cursor
        @param uid: the user id
        @param ids: ids of stock move object to be scrapped
        @param quantity : specify scrap qty
        @param location_id : specify scrap location
        @param context: context arguments
        @return: Scraped lines
        """
        quant_obj = self.pool.get("stock.quant")
        #quantity should be given in MOVE UOM
        if quantity <= 0:
            raise Warning(_('Please provide a positive quantity to scrap.'))
        res = []
        for move in self:
            source_location = move.location_id
            if move.state == 'done':
                source_location = move.location_dest_id
            #Previously used to prevent scraping from virtual location but not necessary anymore
            #if source_location.usage != 'internal':
                #restrict to scrap from a virtual location because it's meaningless and it may introduce errors in stock ('creating' new products from nowhere)
                #raise osv.except_osv(_('Error!'), _('Forbidden operation: it is not allowed to scrap products from a virtual location.'))
            move_qty = move.product_qty
            uos_qty = quantity / move_qty * move.product_uos_qty
            default_val = {
                'location_id': source_location.id,
                'product_uom_qty': quantity,
                'product_uos_qty': uos_qty,
                'state': move.state,
                'scrapped': True,
                'location_dest_id': location_id,
                'restrict_lot_id': restrict_lot_id,
                'restrict_partner_id': restrict_partner_id,
            }
            self._add_move_fields(move, default_val)
            new_move = move.copy(default_val)
            context = self.env.context.copy()

            res += [new_move]
            product_obj = self.env['product.product']
            for product in product_obj.browse([move.product_id.id]):
                if move.picking_id:
                    uom = product.uom_id.name if product.uom_id else ''
                    message = _("%s %s %s has been <b>moved to</b> scrap.") % (quantity, uom, product.name)
                    move.picking_id.message_post(body=message)

            # We "flag" the quant from which we want to scrap the products. To do so:
            #    - we select the quants related to the move we scrap from
            #    - we reserve the quants with the scrapped move
            # See self.action_done, et particularly how is defined the "prefered_domain" for clarification
            scrap_move = self.browse(new_move)
            if move.state == 'done' and scrap_move.location_id.usage not in ('supplier', 'inventory', 'production'):
                domain = [('qty', '>', 0), ('history_ids', 'in', [move.id])]
                # We use scrap_move data since a reservation makes sense for a move not already done
                quants = quant_obj.quants_get_prefered_domain(self.env.cr, self.env.uid, scrap_move.location_id,
                        scrap_move.product_id, quantity, domain=domain, prefered_domain_list=[],
                        restrict_lot_id=scrap_move.restrict_lot_id.id, restrict_partner_id=scrap_move.restrict_partner_id.id, context=context)
                quant_obj.quants_reserve(self.env.cr, self.env.uid, quants, scrap_move)

        for mov in res:
            mov_id = mov.id
            context.update(active_id=mov_id)
            self.pool.get('stock.move').action_done(self.env.cr, self.env.uid,
                                                    [mov_id], context)
        return res
