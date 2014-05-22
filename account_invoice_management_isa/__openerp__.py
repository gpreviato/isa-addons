# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 ISA s.r.l. (<http://www.isa.it>).
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
    'name': 'account invoice managment',
    'version': '0.1',
    'category': 'Generic Modules/Accounting',
    'description': """
        The module allows to force the invoice number by choosing from the invoice numbers deleted
       """,
    'author': 'ISA srl',
    'depends': ['account_invoice_cancel_ext_isa','account_invoice_force_number_ext_isa'],
    'update_xml': [
               'security/managment_group.xml',
               'account_invoice_cancel_isa.xml',
               'invoice_view.xml',
               'account_journal_view.xml',
               'security/ir.model.access.csv'
               
               ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
