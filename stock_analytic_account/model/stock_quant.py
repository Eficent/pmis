# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
import logging


_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',  string="Analytic Account")

    @api.model
    def quants_reserve(self, quants, move, link=False):
        '''If the quant is related to an analytic account other projects
        cannot create moves
        '''
        quants2 = []
        req_analytic_account = move.analytic_account_id
        for quant in quants:
            if quant[0]:
                if req_analytic_account:
                    if quant[0].analytic_account_id and quant[0]. \
                            analytic_account_id != req_analytic_account:
                        continue
                quants2.append(quant)

        # Filter the quants if move has an analytic account
        # quants_2 = filtered(quants)
        return super(StockQuant, self).quants_reserve(quants2, move, link)

    # @api.model
    # def _prepare_account_move_line(self, move, qty, cost,
    #                                credit_account_id, debit_account_id,
    #                                context=None):
    #     res = super(StockQuant,
    #                 self)._prepare_account_move_line(
    #         move, qty, cost,
    #         credit_account_id,
    #         debit_account_id,
    #         context=context
    #     )
    #
    #     # Add analytic account in debit line
    #     if move.analytic_account_id:
    #         res[0][2].update({
    #             'analytic_account_id': move.analytic_account_id.sid,
    #         })
    #     return res

    def _quant_create(self, cr, uid, qty, move, lot_id=False, owner_id=False,
                      src_package_id=False, dest_package_id=False,
                      force_location_from=False, force_location_to=False,
                      context=None):

        new_quant = super(StockQuant, self).\
            _quant_create(cr, uid, qty, move, lot_id, owner_id, src_package_id,
                          dest_package_id, force_location_from,
                          force_location_to, context)

        if move.analytic_account_id.id:
            new_quant.write({'analytic_account_id':
                            move.analytic_account_id.id}
                            )
        return new_quant
