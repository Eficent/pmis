# -*- coding: utf-8 -*-

from openerp import api, fields, models


class AccountAnalyticLinePlan(models.Model):
    _inherit = 'account.analytic.line.plan'

    resource_plan_id = fields.Many2one(
        'analytic.resource.plan.line',
        'Resource Plan Line',
        copy=False,
        ondelete='cascade'
    )
