# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, api, models


class AccountAnalyticAccount(models.Model):

    _inherit = "account.analytic.account"

    move_ids = fields.One2many(
            'stock.move', 'analytic_account_id',
            'Moves for this analytic account')

    use_reserved_stock = fields.Boolean(
            'Use reserved stock',
            help="Stock with reference to this analytic account "
                 "is considered to be reserved."
        )

    @api.one
    def copy(self, default=None):
        """overwrite the copy orm method to clean the produc_ids list.
        """
        default = default or {}
        default['move_ids'] = []
        res = super(AccountAnalyticAccount, self).copy(default)
        return res
