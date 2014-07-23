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
    'name': "Account Incoterm for Intracee",
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Account Incoterm for Intracee
=============================


    """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'depends' : ['account_invoice_intracee',
                 'stock',
                 'stock_makeover',
                 ],
    'data' : [
              'invoice/account_invoice_line_view.xml',
              ],
    'demo' : [],
    'active': False,
    'auto_install': True,
    'installable': True
}
