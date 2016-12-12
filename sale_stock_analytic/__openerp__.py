# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Stock Analytic',
    'version': '8.0.1.0.0',
    'summary': 'Copies the sales order analytic account to the stock move.',
    'author':   'Eficent, '
                'Project Expert Team',
    'contributors': [
        'Jordi Ballester <jordi.ballester@eficent.com>',
    ],
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'images': ['images/deliveries_to_invoice.jpeg'],
    'depends': [
        'sale_stock',
        'stock_analytic_account',
    ],
    'data': [],
    'demo': [],
    'test': [
             ],
    'installable': True,
}
