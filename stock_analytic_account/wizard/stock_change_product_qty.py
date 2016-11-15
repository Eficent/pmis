# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from openerp import api, fields, models


class StockChangeProductQty(models.TransientModel):
    _inherit = "stock.change.product.qty"

    analytic_account_id = fields.Many2one(
            'account.analytic.account', 'Analytic Account')

    @api.multi
    def add_more_fields(self, data, res_original, inventory_id):
        line_data = super(StockChangeProductQty, self).\
            add_more_fields(data, res_original, inventory_id)
        line_data.update(analytic_account_id=data.analytic_account_id.id)
        return line_data
