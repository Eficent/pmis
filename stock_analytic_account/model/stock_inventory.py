# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.tools.translate import _
import logging


_logger = logging.getLogger(__name__)


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    def onchange_filter(self, filter):
        to_clean = super(StockInventory, self).onchange_filter(filter)
        if filter != 'analytic':
            to_clean['value']['analytic_account_id'] = False
        return to_clean


    @api.model
    def _get_available_filters(self):
        """This function will return the list of filters allowed according to
        the options checked in 'Settings/Warehouse'.

        :return: list of tuple
        """
        res_filters = super(StockInventory, self)._get_available_filters()
        res_filters.append(('analytic', _('One Analytic Account')))
        return res_filters

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',  string="Analytic Account")
    filter = fields.Selection(
        selection=_get_available_filters, string='Selection Filter',
        required=True)

    @api.model
    def _get_inventory_lines_domain_hook(self, inventory):
        domain = super(StockInventory, self)._get_inventory_lines_domain_hook(
            inventory)
        if not inventory.analytic_account_id.id:
            return domain or ""
        if domain:
            domain += ' and analytic_account_id = %s'
        else:
            domain = ' and analytic_account_id = %s'
        return domain


    @api.model
    def _get_inventory_lines_args_hook(self, inventory):
        args = super(StockInventory, self)._get_inventory_lines_args_hook(
            inventory)
        if not inventory.analytic_account_id.id:
            return args or (tuple([]))
        if args:
            args += tuple(inventory.analytic_account_id.id)
        else:
            args = (tuple([inventory.analytic_account_id.id]),)
        return args


    @api.model
    def _get_inventory_lines_query_select(self):
        query_select = super(StockInventory, self). \
            _get_inventory_lines_query_select()
        query_select += ', analytic_account_id'
        return query_select


    @api.model
    def _get_inventory_lines_query_group_by(self):
        group_by = super(StockInventory, self). \
            _get_inventory_lines_query_group_by()
        if group_by:
            group_by += ", analytic_account_id"
        return group_by


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',  string="Analytic Account")

    @api.model
    def inventory_line_domain(self, line):
        domain, message = super(StockInventoryLine, self).inventory_line_domain(
            line)
        if domain:
            domain.append(('analytic_account_id', '=',
                           line.analytic_account_id.id), )
        else:
            domain = [('analytic_account_id', '=',
                       line.analytic_account_id.id)]

        message = _("You cannot have two inventory adjustements in state "
                    "'in Progress' with the same product(%s), same "
                    "location(%s), same package, same owner and lot and same "
                    "analytic account. Please first validate the first "
                    "inventory adjustement with this product before creating "
                    "another one."
                    % (line.product_id.name, line.location_id.name))
        return domain, message
