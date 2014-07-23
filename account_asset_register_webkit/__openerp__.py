# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ISA s.r.l. (<http://www.isa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Account Asset Register - Libro Cespiti',
    'version': '0.1',
    'author': "ISA srl",
    'website': 'http://www.isa.it',
    'category': 'Generic Modules/Accounting',
    'description': """
Libro Cespiti
=============

Managing the printing of the "Assets Register".

Gestione della stampa del "Libro dei Cespiti".

""",
    'depends' : [
        'report_webkit',
        'account_asset',
        'account_financial_report_webkit',
        ],
    'data': [
        'report/report.xml',
        'wizard/account_asset_report.xml',
        'account_fiscalyear_view.xml',
        ],
    'demo': [],
    'test':[],
    'installable': True,
    'auto_install': True,
    'certificate': '',
}
