# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 ISA s.r.l. (<http://www.isa.it>).
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
    'name': "Payments Due list Report Webkit",
    'version': '0.1',
    'category': 'Generic Modules/Payment',
    'description': """

Report of a due list of pending payments.
The list contains every expected payment, generated by invoices.
""",
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'license': 'AGPL-3',
    "depends" : [
                 'account',
                 'account_due_list',
                 'report_webkit',
                 'account_financial_report_webkit',
                ],
    "data" : [
              'wizard/due_list_view.xml',
              'report/report.xml',
             ],
    "demo" : [],
    "installable": True
}
