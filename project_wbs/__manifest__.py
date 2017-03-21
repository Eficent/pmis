# -*- coding: utf-8 -*-
{
    'name': 'Work Breakdown Structure',
    'version': '1.0',
    'author': 'Deneroteam. <dhaval@deneroteam.com>',
    'website': 'http://deneroteam.com/',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'depends': [
        'project',
        'account',
        'analytic',
        'project_issue',
        'web_one2many_kanban'
    ],
    'summary': 'Project Work Breakdown Structure',
    'data': [
        'data/data.xml',
        'view/account_analytic_account_view.xml',
        'view/project_project_view.xml',
        # 'view/project_configuration.xml',
        # 'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'css': [
        'static/src/css/project_kanban.css',
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
}
