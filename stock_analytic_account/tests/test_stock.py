# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp.addons.stock.tests.common import TestStockCommon


class TestStockMove(TestStockCommon):

    def setUp(self):
        super(TestStockMove, self).setUp()
        self.ResUsers = self.env['res.users']
        self.WarehouseObj = self.env['stock.warehouse']
        self.LocationObj = self.env['stock.location']
        self.InventoryObj = self.env['stock.inventory']
        self.InventoryLineObj = self.env['stock.inventory.line']
        self.StockQuant = self.env['stock.quant']
        self.ProductTemplateObj = self.registry['product.template']
        self.ProductCatObj = self.registry['product.category']
        self.ChangePrice = self.registry('stock.change.standard.price')
        # company
        self.company1 = self.env.ref('base.main_company')
        # groups
        self.group_stock_manager = self.env.ref('stock.group_stock_manager')
        # Products
        self.product1 = self.env.ref('product.product_product_7')
        self.product2 = self.env.ref('product.product_product_9')
        self.product3 = self.env.ref('product.product_product_11')
        self.apple_cat = self.env.ref('product.accessories')
        self.location1 = self.env.ref('stock.location_inventory')
        self.inv1 = self.create_adjustment('product1 inventory', self.product1)

    def count_quants(self, inv):
        qty = 0
        for line in inv.line_ids:
            product_qty = line._get_theoretical_qty('name', False)
            if line.id in product_qty:
                qty += product_qty[line.id]
        return qty

    def _create_inv_lines(self, product_id, inv_id):
        inv_line = self.InventoryLineObj.create({
            'product_id': product_id,
            'inventory_id': inv_id,
            'location_id': self.location1.id
        })
        inv_line.write({'product_qty': inv_line.theoretical_qty + 10})

    def create_adjustment(self, name, product):
        inv = self.InventoryObj.create({
            'name': name,
            'product_id': product.id,
            'filter': 'product',
            'location_id': self.location1.id
        })
        inv.prepare_inventory()
        self._create_inv_lines(product.id, inv.id)
        return inv

    def test_change_price(self):
        self.apple_cat.write({
            'property_stock_account_input_categ': 56,
            'property_stock_account_output_categ': 44,
        })
        self.product2.product_tmpl_id.do_change_standard_price(1500)
        self.assertEqual(self.product2.standard_price, 1500)

    def test_inventory_adjustment(self):
        prev_quants = self.count_quants(self.inv1)
        self.inv1.action_check()
        self.InventoryObj.post_inventory(self.inv1)
        new_quants = self.count_quants(self.inv1)
        self.assertNotEqual(prev_quants, new_quants)
