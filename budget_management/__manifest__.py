{
    'name': "Budget",
    'version': "1.0",
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/budget_automatic_entry_wizard_views.xml',
        'views/budget_budget_view.xml',
        'views/budget_line_view.xml',
        'views/budget_budget_menu.xml',
    ],

    'installable': True,
    'application': True,
    'license': "LGPL-3",
}
