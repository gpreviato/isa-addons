# -*- encoding: utf-8 -*-

{
    'name': 'Isa accounting reports Layout generic Invoice (no picking)',
    'version': '0.1',
    'category': 'report',
    'description': """Accounting Isa reports - Fattura generica layout
    Install report_aero_ooo to be able to output to a format
    different from the one of the template.
    """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'license': 'AGPL-3',
    "depends" : ['account_invoice_layout','l10n_it_account', 'report_aeroo_ooo'],
    "init_xml" : [
        ],
    "update_xml" : [
        'reports.xml',
        ],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
