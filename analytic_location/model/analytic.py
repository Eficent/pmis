# -*- coding: utf-8 -*-
# © 2014-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Matmoz d.o.o.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.model
    def _default_warehouse(self):
        warehouse_obj = self.env['stock.warehouse']
        company_obj = self.env['res.company']
        company_id = company_obj._company_default_get('stock.warehouse')
        warehouse_ids = warehouse_obj.search(
            [('company_id', '=', company_id)], limit=1) or []
        if warehouse_ids:
            return warehouse_ids[0]
        else:
            return False

    @api.model
    def _default_dest_address(self):
        partner_id = self.env.context.get('partner_id', False)
        if partner_id:
            return self.env['res.partner'].address_get(
                [partner_id], ['delivery']
            )['delivery'],
        else:
            return False

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        'Warehouse', default=_default_warehouse)
    location_id = fields.Many2one(
        'stock.location',
        'Default Stock Location',
        domain=[('usage', '<>', 'view')])
    dest_address_id = fields.Many2one(
        'res.partner',
        'Delivery Address',
        default=_default_dest_address,
        help="Delivery address for "
        "the current contract "
        "/project.")
