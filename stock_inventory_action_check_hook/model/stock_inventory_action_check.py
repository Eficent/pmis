# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _
import logging


_logger = logging.getLogger(__name__)


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _inventory_action_check_hook(self, inventory_line, move_vals):
        """ Creates a stock move from an inventory line
        @param inventory_line:
        @param move_vals:
        @return:
        """
        if inventory_line.analytic_account_id:
            move_vals['analytic_account_id'] = \
                inventory_line.analytic_account_id.id

        move = self.env['stock.move'].create(move_vals)
        return move

    @api.multi
    def action_check(self):
        """ Confirm the inventory and writes its finished date
        Attention!!! This method overrides the standard without calling Super
        The changes introduced by this module are encoded within a
        comments START OF and END OF stock_analytic_account.
        @return: True
        """
        # to perform the correct inventory corrections we need analyze
        # stock location by
        # location, never recursively, so we use a special context
        self = self.with_context(dict(self.env.context, compute_child=False))

        product_obj = self.env['product.product']
        for inv in self:
            move_ids = []
            moves = []
            for line in inv.line_ids:
                pid = line.product_id.id
                # START OF stock_analytic_account
                # Replace the existing entry:
                # product_context.update(uom=line.product_uom.id,
                # to_date=inv.date,
                # date=inv.date, prodlot_id=line.prod_lot_id.id)
                # ,with this one:
                self = self.with_context(
                    uom=line.product_uom_id.id, to_date=inv.date, date=inv.date,
                    prodlot_id=line.prod_lot_id.id,
                    analytic_account_id=line.analytic_account_id.id,
                )
                # ENF OF stock_analytic_account
                res = product_obj._product_available(
                    [pid], None, False)[pid]
                change = line.product_qty - res['qty_available']
                lot_id = line.prod_lot_id.id
                # analytic_account_id = line.analytic_account_id.id or False
                if change:
                    location_id = line.product_id.property_stock_inventory.id
                    value = {
                        'name': _('INV:') + (line.inventory_id.name or ''),
                        'product_id': line.product_id.id,
                        'product_uom': line.product_uom_id.id,
                        'prodlot_id': lot_id,
                        'date': inv.date,
                    }

                    if change > 0:
                        value.update({
                            'product_uom_qty': change,
                            'location_id': location_id,
                            'location_dest_id': line.location_id.id,
                        })
                    else:
                        value.update({
                            'product_uom_qty': -change,
                            'location_id': line.location_id.id,
                            'location_dest_id': location_id,
                        })
                    move = self._inventory_action_check_hook(
                        line, value)
                    moves.append(move)
                    move_ids.append(move.id)
            inv.write({'state': 'confirm',
                      'move_ids': [(6, 0, move_ids)]})
            for move in moves:
                move.action_confirm()
            # self.env['stock.move'].action_confirm(move_ids)
        return True


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',  string="Analytic Account")

    @api.model
    def _get_quants(self, line):
        quant_obj = self.env["stock.quant"]
        dom = [('company_id', '=', line.company_id.id), ('location_id', '=', line.location_id.id), ('lot_id', '=', line.prod_lot_id.id),
                        ('product_id','=', line.product_id.id), ('owner_id', '=', line.partner_id.id), ('package_id', '=', line.package_id.id),
                        ('analytic_account_id', '=', line.analytic_account_id.id)]
        quants = quant_obj.search(dom)
        quant_ids =[]
        for quant in quants:
            quant_ids.append(quant.id)
        return quant_ids

    @api.one
    @api.onchange('product_id', 'location_id', 'product_uom_id',
                  'analytic_account_id', 'location_id', 'package_id',
                  'partner_id')
    def onchange_line(self):
        quant_obj = self.env["stock.quant"]
        uom_obj = self.env["product.uom"]
        res = {'value': {}}
        # If no UoM already put the default UoM of the product
        if self.product_id:
            product = self.product_id
            uom = self.product_uom_id
            if product.uom_id.category_id.id != uom.category_id.id:
                self.product_uom_id = product.uom_id.id
                res['domain'] = {
                    'product_uom_id': [('category_id', '=',
                                        product.uom_id.category_id.id)]}
        # Calculate theoretical quantity by searching the quants as in
        # quants_get
        if self.product_id and self.location_id:
            product = self.product_id
            company_id = self.env['res.users'].browse(self._uid).\
                company_id.id
            dom = [('company_id', '=', company_id),
                   ('location_id', '=', self.location_id.id),
                   ('lot_id', '=', self.prod_lot_id.id),
                   ('product_id', '=', self.product_id.id),
                   ('owner_id', '=', self.partner_id.id),
                   ('package_id', '=', self.package_id.id),
                   ('analytic_account_id', '=', self.analytic_account_id.id)]
            quants = quant_obj.search(dom)
            th_qty = sum([x.qty for x in quants])
            if self.product_id and self.product_uom_id and\
                product.uom_id.id != self.product_uom_id:
                    th_qty = uom_obj._compute_qty(product.uom_id.id, th_qty,
                                              self.product_uom_id.id)
            self.theoretical_qty = th_qty
            self.product_qty = th_qty
