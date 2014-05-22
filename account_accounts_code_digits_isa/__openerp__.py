# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2013 ISA srl (<http://www.isa.it>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Account code digits Isa',
    'version': '0.1',
    "category": 'Accounting & Finance',
    'description': """
        The module pre-fills the digits for the accounts of the accounting plan: eg. 6 - 101001.
        Alla creazione di un conto sul pdc il modulo recupera in AUTOMATICO il codice del mastro e gruppo selezionati e propone l'ultimo progressivo numerico disponibile (comunque editabile).
       """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'license': 'AGPL-3',
    "depends" : ['account'],
    "init_xml" : [],
    'update_xml': ['account_accounts_code_digits_isa_view.xml',
                   'partner_isa_view.xml'],
    "demo_xml" : [],
    "active": False,
    "installable": True,
    'certificate': '',
}
