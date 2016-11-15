# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _prepare_order_line_procurement(self, line, group_id=False):
        res = super(
            SaleOrder, self)._prepare_order_line_procurement(line, group_id)
        if self.project_id:
            res['analytic_account_id'] = self.project_id.id
        return res


class ProcuerementOrder(models.Model):
    _inherit = "procurement.order"

    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic account')

    @api.one
    def _run_move_create(self):
        res = super(
            ProcuerementOrder, self)._run_move_create()
        if self.analytic_account_id:
            res['analytic_account_id'] = self.analytic_account_id.id
        return res
