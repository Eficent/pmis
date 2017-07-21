# -*- coding: utf-8 -*-

{
    'name': 'Analytic Resource Planning',
    'version': '9.0.1.0.0',
    'author':   'Eficent, '
                'Matmoz, '
                'Luxim, '
                'Project Expert Team',
    'website': 'http://project.expert',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': ['account', 'purchase', 'analytic_plan'],
    'data': [
        'view/account_analytic_plan_version_view.xml',
        'view/analytic_resource_plan_view.xml',
        'view/analytic_account_view.xml',
        'view/product_view.xml',
        'view/project_view.xml',
        'view/resource_plan_default.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
