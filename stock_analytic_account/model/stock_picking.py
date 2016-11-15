# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    analytic_account_ids = fields.Many2one(
            related='move_lines.analytic_account_id',
            relation='account.analytic.account', string='Analytic Account',
            readonly=True
        )
    analytic_account_user_ids = fields.Many2one(
            related='move_lines.analytic_account_user_id',
            relation='res.users',
            string='Project Manager',
            readonly=True
        )
