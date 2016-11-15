# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.model
    def _get_quant_domain(self):
        domain = super(ProductProduct, self)._get_quant_domain()
        context = self.env.context or {}
        analytic_account_id = self.env.context.get('analytic_account_id', False)
        if domain and analytic_account_id:
            return [('analytic_account_id', '=', analytic_account_id)]
        else:
            return []

    @api.multi
    def _get_move_in_domain(self):
        domain = super(ProductProduct, self)._get_move_in_domain()
        analytic_account_id = self.env.context.get('analytic_account_id', False)
        if domain and analytic_account_id:
            domain.append(('analytic_account_id', '=', analytic_account_id))
        else:
            domain = ('analytic_account_id', '=', analytic_account_id)
        return domain

    @api.multi
    def _get_move_out_domain(self):
        domain = super(ProductProduct, self)._get_move_out_domain()
        analytic_account_id = self.env.context.get('analytic_account_id', False)
        if domain and analytic_account_id:
            domain.append(('analytic_account_id', '=', analytic_account_id))
        else:
            domain = ('analytic_account_id', '=', analytic_account_id)
        return domain
