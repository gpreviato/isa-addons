# -*- encoding: utf-8 -*-
##############################################################################
#
#    Authors: Nicolas Bessi, Guewen Baconnier
#    Copyright Camptocamp SA 2011
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
    'name': 'Report Estratti Conto - Webkit',
    'description': """
Report Estratti Conto - Webkit
==============================

This module adds the following standard OpenERP financial reports:
 - Estratti Conto per Partita

""",
    'version': '0.0.1',
    'author': 'ISA srl',
    'license': 'AGPL-3',
    'category': 'Finance',
    'website': 'http://www.isa.it',
    'images': [
        'images/ledger.png',],
    'depends': ['account',
                'account_ricevute_bancarie',
                'account_financial_report_webkit',
                'report_webkit'],

    'demo' : [],
    'data': [
               'data/financial_webkit_header.xml',
               'report/report.xml',
               'wizard/wizard.xml',
               'wizard/account_statement_wizard.xml',
               ],

    'test': [],

    'active': False,
    'installable': True,
    'application': True,
}
