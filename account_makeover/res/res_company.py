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

from openerp.osv import fields, orm

class res_company_isa(orm.Model):
    _inherit = 'res.company'
    _columns = {
                'subaccount_auto_generation_customer': fields.boolean('Customers Subaccount Automatic Generation'),
                'subaccount_auto_generation_supplier': fields.boolean('Suppliers Subaccount Automatic Generation'),
                'account_parent_customer': fields.many2one('account.account',
                                                           'Customers Ledger',
                                                           ),
                'account_parent_supplier': fields.many2one('account.account',
                                                           'Suppliers Ledger',
                                                           ),
                }
