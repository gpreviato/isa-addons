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
    'name': 'account invoice bank per partner ext ISA',
    'version': '0.1',
    'category': '',
    'description': """
            Personalizzazioni modulo fattura con aggiunta del conto del cliente.
            
            Il campo Banca Cliente si riferisce solo ai conti bancari del cliente.
            Il campo Banca Azienda si riferisce solo ai conti bancari dell'azienda.
            
            Per visualizzare il campo 'Banca Azienda' assicurarsi di avere i permessi:
              - - -  Autorizzazioni accesso -> Usability -> Analytic Accounting : true
       """,
    'author': 'ISA srl',
    'depends': ['account','account_invoice_ext_isa',],
    'update_xml': ['account_invoice_bank_partner_ext_isa_view.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
