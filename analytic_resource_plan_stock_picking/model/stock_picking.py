# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_resource_plan_line_id = fields.Many2one(
        'analytic.resource.plan.line',
        "Resource Plan Line",
        readonly=True
    )
