# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Stock Analytic Account',
    'version': '8.0.1.0.1',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['stock', 'analytic', 'stock_analytic',
                'product_available_hook',
                'stock_get_inventory_lines_hook',
                'stock_inventory_action_check_hook',
                'stock_action_scrap_hook',
                'stock_change_product_qty_hook',
                'stock_analytic_reserve',
                'sale_stock'],
    'data': [
             'view/stock_view.xml',
             'view/stock_picking_view.xml',
             'view/analytic_account_view.xml',
             'view/stock_warehouse_view.xml',
             # 'report/report_stock_analytic_account_view.xml',
             # 'report/report_stock_move_view.xml',
             'wizard/stock_change_product_qty_view.xml',
    ],

    'installable': True,
    'active': False,
    'certificate': '',
}
