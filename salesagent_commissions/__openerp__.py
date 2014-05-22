# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'SalesAgent Commission module',
    'version': '0.2',
    'category': 'Account',
    'description': """
        [ITA] Modulo per la gestione degli agenti di vendita
        [ENG] Module to manage salesagent
        """,
    'author': 'www.andreacometa.it',
    'website': 'http://www.andreacometa.it',
    'license': 'AGPL-3',
    "active": False,
    "installable": True,
    "depends" : ['base', 'product', 'account'],
    "update_xml" : [
        'salesagent_view.xml',
        'partner/partner_view.xml',
        'product/product_view.xml',
        'account/account_view.xml',
        'wizard/wizard_view.xml',
        ],
}
