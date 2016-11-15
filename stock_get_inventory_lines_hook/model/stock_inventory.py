# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _
from openerp.exceptions import Warning


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.model
    def _get_inventory_lines_domain_hook(self, inventory):
        return False

    @api.model
    def _get_inventory_lines_args_hook(self, inventory):
        return False

    @api.model
    def _get_inventory_lines_query_select(self):
        return """product_id, sum(qty) as product_qty,
            location_id, lot_id as prod_lot_id, package_id,
            owner_id as partner_id"""

    @api.model
    def _get_inventory_lines_query_from(self):
        return """stock_quant"""

    @api.model
    def _get_inventory_lines_query_where(self, domain):
        return domain

    @api.model
    def _get_inventory_lines_query_group_by(self):
        return """product_id, location_id, lot_id, package_id, partner_id"""""

    @api.model
    def _get_inventory_lines_query_hook(self, domain):

        q_select = self._get_inventory_lines_query_select()
        q_from = self._get_inventory_lines_query_from()
        q_where = self._get_inventory_lines_query_where(domain)
        q_group_by = self._get_inventory_lines_query_group_by()

        query = """SELECT %s FROM %s WHERE %s GROUP BY %s""" % (
            q_select, q_from, q_where, q_group_by)
        return query

    @api.model
    def _get_inventory_lines(self, inventory):
        location_obj = self.env['stock.location']
        product_obj = self.env['product.product']
        location_ids = location_obj.search([('id', 'child_of',
                                            inventory.location_id.id)])
        domain = ' location_id in %s'
        args = (tuple(location_ids.ids),)
        if inventory.partner_id:
            domain += ' and owner_id = %s'
            args += (inventory.partner_id.id,)
        if inventory.lot_id:
            domain += ' and lot_id = %s'
            args += (inventory.lot_id.id,)
        if inventory.product_id:
            domain += ' and product_id = %s'
            args += (inventory.product_id.id,)
        if inventory.package_id:
            domain += ' and package_id = %s'
            args += (inventory.package_id.id,)
        domain += self._get_inventory_lines_domain_hook(inventory)
        args += self._get_inventory_lines_args_hook(inventory)

        query = self._get_inventory_lines_query_hook(domain)
        self.env.cr.execute(query, args)

        vals = []
        for product_line in self.env.cr.dictfetchall():
            # replace the None the dictionary by False, because falsy
            # values are tested later on
            for key, value in product_line.items():
                if not value:
                    product_line[key] = False
            product_line['inventory_id'] = inventory.id
            product_line['theoretical_qty'] = product_line['product_qty']
            if product_line['product_id']:
                product = product_obj.browse(product_line['product_id'])
                product_line['product_uom_id'] = product.uom_id.id
            vals.append(product_line)
        return vals


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.model
    def inventory_line_domain(self, line):
        domain = [
            ('product_id', '=', line.product_id.id),
            ('location_id', '=', line.location_id.id),
            ('inventory_id.state', '=', 'confirm'),
            ('prod_lot_id', '=', line.prod_lot_id.id),
            ('partner_id', '=', line.partner_id.id),
            ('package_id', '=', line.package_id.id),
            ('id', 'not in', self.ids)
        ]
        message = _("You cannot have two inventory adjustements in state "
                    "'in Progress' with the same product(%s), same "
                    "location(%s), same package, same owner and same lot. "
                    "Please first validate the first inventory adjustement "
                    "with this product before creating another one."
                    % (line.product_id.name, line.location_id.name))
        return domain, message

    @api.multi
    @api.constrains('product_id', 'location_id', 'inventory_id',
                    'lot_id', 'partner_id', 'package_id')
    def _check_inventory_line(self):
        """Refuse to record duplicate inventory lines
        Inventory lines with the sale Product, Location, Serial Number,
        as it is done in the standard"""
        for line in self:
            dom, err = self.inventory_line_domain(line)
            res = self.search(dom)
            if res:
                raise Warning(err)

    @api.model
    def create(self, values):
        return models.Model.create(self, values)
