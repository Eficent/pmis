# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from openerp.tools.translate import _
from openerp import tools
from openerp.exceptions import Warning

class StockChangeProductQty(models.TransientModel):
    _inherit = "stock.change.product.qty"

    @api.multi
    def add_more_fields(self, data, res_original, inventory_id):
        if res_original.uom_id:
            uom = res_original.uom_id.id
        else:
            False
        line_data = {
            'inventory_id': inventory_id.id,
            'product_qty': data.new_quantity,
            'location_id': data.location_id.id,
            'product_id': data.product_id.id,
            'product_uom_id': uom,
        }
        return line_data

    @api.multi
    def _prepare_inventory_hook(self, data, search_filter):
        return {
                'name': _('INV: %s') % tools.ustr(data.product_id.name),
                'filter': search_filter,
                'product_id': data.product_id.id,
                'location_id': data.location_id.id,
                'lot_id': data.lot_id.id}

    @api.multi
    def change_product_qty(self):
        """ Changes the Product Quantity by making a Physical Inventory.
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: List of IDs selected
        @param context: A standard dictionary
        @return:
        """
        context = self.env.context.copy()
        if context is None:
            context = {}

        rec_id = context and context.get('active_id', False)
        assert rec_id, _('Active ID is not set in Context')

        inventory_obj = self.env['stock.inventory']
        inventory_line_obj = self.env['stock.inventory.line']
        prod_obj_pool = self.env['product.template']

        res_original = prod_obj_pool.browse(rec_id)
        for data in self:
            if data.new_quantity < 0:
                raise Warning(_('Quantity cannot be negative.'))

            search_filter = 'none'
            if data.product_id.id and data.lot_id.id:
                search_filter = 'none'
            elif data.product_id.id:
                search_filter = 'product'

            inventory_data = self._prepare_inventory_hook(data, search_filter)
            inventory_id = inventory_obj.create(inventory_data)

            line_data = self.add_more_fields(data, res_original, inventory_id)

            inventory_line_obj.create(line_data)
            inventory_id.action_check()
            inventory_id.action_done()
        return {}
