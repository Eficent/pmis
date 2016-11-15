# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models
from openerp.tools.float_utils import float_round


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.multi
    def _get_move_in_domain(self):
        return []

    @api.multi
    def _get_move_out_domain(self):
        return []

    @api.model
    def _get_quant_domain(self):
        return []

    @api.model
    def _product_available(self, products, field_names=None, arg=False):
        context = self.env.context or {}
        field_names = field_names or []

        domain_products = [('product_id', 'in', products)]
        domain_move_in, domain_move_out = [], []
        domain_quant = self._get_quant_domain()

        domain_quant_loc, domain_move_in_loc, domain_move_out_loc = \
            self._get_domain_locations()
        domain_move_in += self._get_domain_dates() + \
            [('state', 'not in', ('done', 'cancel', 'draft'))] + \
            domain_products
        domain_move_out += self._get_domain_dates() + \
            [('state', 'not in', ('done', 'cancel', 'draft'))] + \
            domain_products
        domain_quant += domain_products

        if context.get('lot_id'):
            domain_quant.append(('lot_id', '=', context['lot_id']))
        if context.get('owner_id'):
            domain_quant.append(('owner_id', '=', context['owner_id']))
            owner_domain = ('restrict_partner_id', '=', context['owner_id'])
            domain_move_in.append(owner_domain)
            domain_move_out.append(owner_domain)
        if context.get('package_id'):
            domain_quant.append(('package_id', '=', context['package_id']))

        appended_domain = self._get_move_in_domain()
        if len(appended_domain) > 0:
            domain_move_in.append(appended_domain)
        appended_domain = self._get_move_out_domain()
        if len(appended_domain) > 0:
            domain_move_out.append(appended_domain)

        domain_move_in += domain_move_in_loc
        domain_move_out += domain_move_out_loc
        moves_in = self.env['stock.move'].read_group(
            domain_move_in, ['product_id', 'product_qty'], ['product_id'])
        moves_out = self.env['stock.move'].read_group(
            domain_move_out, ['product_id', 'product_qty'], ['product_id'])

        domain_quant += domain_quant_loc
        quants = self.env['stock.quant'].read_group(
            domain_quant, ['product_id', 'qty'], ['product_id'])
        quants = dict(map(lambda x: (x['product_id'][0], x['qty']), quants))

        moves_in = dict(map(lambda x: (x['product_id'][0], x['product_qty']),
                            moves_in))
        moves_out = dict(map(lambda x: (x['product_id'][0], x['product_qty']),
                             moves_out))
        res = {}
        for product in self.env['product.product'].browse(products):
            qty_available = float_round(quants.get(product.id, 0.0),
                                        precision_rounding=product.uom_id.rounding)
            incoming_qty = float_round(moves_in.get(product.id, 0.0),
                                       precision_rounding=product.uom_id.rounding)
            outgoing_qty = float_round(moves_out.get(product.id, 0.0),
                                       precision_rounding=product.uom_id.rounding)
            virtual_available = float_round(
                quants.get(product.id, 0.0) + moves_in.get(product.id, 0.0) -
                moves_out.get(product.id, 0.0),
                precision_rounding=product.uom_id.rounding)
            res[product.id] = {
                'qty_available': qty_available,
                'incoming_qty': incoming_qty,
                'outgoing_qty': outgoing_qty,
                'virtual_available': virtual_available,
            }
        return res
