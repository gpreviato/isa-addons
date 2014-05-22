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


from osv import fields, osv
from tools.translate import _



class account_accounts_code_digits_ext_isa(osv.osv):
    _inherit = 'account.account'
    
    def _default_type_from_partner(self, cr, uid, context=None):
        if ((context.has_key('customer'))& (context.has_key('supplier'))):
            return 'view'
        else:
            if (context.has_key('customer')):
                return 'receivable'
            else:
                if (context.has_key('supplier')):
                    return 'payable'
                else:
                    return 'view'
     
    def _default_user_type_from_partner(self, cr, uid, context=None):
        account_type_obj = self.pool.get('account.account.type')
        isset_account_type=False
        if (context.has_key('customer')):
            isset_account_type=account_type_obj.search(cr, uid,[('code', '=', 'receivable')])
        else:
            if (context.has_key('supplier')):
                isset_account_type=account_type_obj.search(cr, uid,[('code', '=', 'payable')])
        
        if(isset_account_type):
            return str(isset_account_type[0])
        return ''
                
    def _default_reconcile_from_partner(self, cr, uid, context=None):
        if ((context.has_key('customer')) | (context.has_key('supplier'))):
            return True
        else:
            return False
        
    def _default_name_from_partner(self, cr, uid, context=None):
        if (context.has_key('partner_name')):
            if (context['partner_name']):
                return str(context['partner_name'])
        return ''  

    _defaults = {
        'code': '',
        'type': _default_type_from_partner,
        'user_type': _default_user_type_from_partner,
        'reconcile': _default_reconcile_from_partner,
        'name': _default_name_from_partner,
     
    }
    
    def onchange_parent_id(self, cr, uid, ids, parent_id):
        if not parent_id:
            return {}
        #import pdb;pdb.set_trace()
        reads = self.read(cr, uid, parent_id, ['code'])
        res = {}
        if reads['code']:

            cr.execute("SELECT MAX(code) "\
                       "FROM account_account "\
                       "WHERE CAST(code AS TEXT) "\
                       "LIKE '" + reads['code'] + "%'")
            max_code = cr.fetchall()[0][0]

            wizard_accounts_obj = self.pool.get('wizard.multi.charts.accounts')
            wizard_accounts_ids = wizard_accounts_obj.search(cr, uid, [])
            str_pad_res = wizard_accounts_obj.read(cr, uid, wizard_accounts_ids, ['code_digits'])
            res ={}
            if (len(str_pad_res)):
                str_pad = str_pad_res[0]['code_digits']
                max_code = max_code.ljust(str_pad, '0')
                max_code = str(int(max_code) +1)
                max_code = max_code.rjust(str_pad, '0');            
                res = {'value':{'code': max_code }}

            return res

account_accounts_code_digits_ext_isa()
    
    


