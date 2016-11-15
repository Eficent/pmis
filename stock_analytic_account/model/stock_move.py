# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class StockMove(models.Model):

    _inherit = "stock.move"

    # analytic_account_id = fields.Many2one(
    #     comodel_name='account.analytic.account',  string="Analytic Account")

    analytic_account_user_id = fields.Many2one(
        comodel_name='res.users', string='Project Manager', store=True,
        readonly=True, related='analytic_account_id.user_id')

    analytic_reserved = fields.Boolean(
        'Reserved', help="Reserved for the Analytic Account")

    @api.model
    def _get_analytic_reserved(self, vals):
        analytic_obj = self.env['account.analytic.account']
        aaid = vals['analytic_account_id']
        if aaid:
            aa = analytic_obj.browse(aaid)
            return aa.use_reserved_stock
        else:
            return False

    @api.model
    def create(self, values):
        if 'analytic_account_id' in values:
            values['analytic_reserved'] = self._get_analytic_reserved(values)
        return super(StockMove, self).create(values)

    @api.multi
    def write(self, values):
        if 'analytic_account_id' in values:
            values['analytic_reserved'] = self._get_analytic_reserved(values)
        return super(StockMove, self).write(values)

    @api.model
    def _add_move_fields(self, move, default_val):
        default_val = super(StockMove, self)._add_move_fields(self, default_val)
        default_val.update(analytic_account_id=move.analytic_account_id.id)
        return default_val
