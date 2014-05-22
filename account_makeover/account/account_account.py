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

from openerp.osv import orm, fields

class account_account_ext_isa(orm.Model):
    _inherit = 'account.account'
    
    def _default_type_from_partner(self, cr, uid, context=None):
        if (('customer' in context) & ('supplier' in context)):
            return 'view'
        else:
            if ('customer' in context):
                return 'receivable'
            else:
                if ('supplier' in context):
                    return 'payable'
                else:
                    return 'view'
     
    def _default_user_type_from_partner(self, cr, uid, context=None):
        type_obj = self.pool.get('account.account.type')
        isset_account_type = False
        if ('customer' in context):
            isset_account_type = type_obj.search(cr, uid,
                                            [('code', '=', 'receivable')])
        else:
            if ('supplier' in context):
                isset_account_type = type_obj.search(cr, uid,
                                            [('code', '=', 'payable')])
        
        if(isset_account_type):
            return str(isset_account_type[0])
        return ''
                
    def _default_reconcile_from_partner(self, cr, uid, context=None):
        if (('customer' in context) | ('supplier' in context)):
            return True
        else:
            return False
        
    def _default_name_from_partner(self, cr, uid, context=None):
        if ('partner_name' in context):
            if (context['partner_name']):
                return context['partner_name']
        return ''  
    
    _columns = {
                'partner_id': fields.many2one('res.partner',
                                              'Partner')
                }

    _defaults = {
        'code': '',
        'type': _default_type_from_partner,
        'user_type': _default_user_type_from_partner,
        'reconcile': _default_reconcile_from_partner,
        'name': _default_name_from_partner,
     
    }

    def get_max_code(self, cr, uid, ids, parent_id):
        reads = self.read(cr, uid, parent_id, ['code'])
        max_code = None
        if reads['code']:
            cr.execute("SELECT MAX(code) "
                "FROM account_account "
                "WHERE CAST(code AS TEXT) "
                "LIKE '" + 
                reads['code'] + "%'")
            max_code = cr.fetchall()[0][0]

            acc_obj = self.pool.get('account.config.settings')
            accounts_ids = acc_obj.search(cr, uid, [])
            if not accounts_ids:
                acc_obj = self.pool.get('wizard.multi.charts.accounts')
                accounts_ids = acc_obj.search(cr, uid, [])
            if not accounts_ids:
                acc_obj = self.pool.get('account.chart.template')
                accounts_ids = acc_obj.search(cr, uid, [('name', '=', 'Italy - Generic Chart of Accounts')])
            str_pad_res = acc_obj.read(cr, uid, accounts_ids, ['code_digits'])
            if (len(str_pad_res)):
                str_pad = str_pad_res[0]['code_digits']
                max_code = max_code.ljust(str_pad, '0')
                max_code = str(int(max_code) + 1)
                max_code = max_code.rjust(str_pad, '0')

        return max_code

    def onchange_parent_id(self, cr, uid, ids, parent_id):
        if not parent_id:
            return {}
        max_code = None
        if not ids:
            max_code = self.get_max_code(cr, uid, ids, parent_id)

            return {'value': {'code': max_code}}
        return {'value': {}}

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        if isinstance(ids, (int, long)):
                    ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code', 'company_id'], context=context)
        res = []
        t_company_dict = {}
        for t_data in reads:
            if t_data['company_id']:
                t_company_dict.update({t_data['company_id'][0]: True})
            if len(t_company_dict)>1:
                break
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' ' + name
                if record['company_id'] and len(t_company_dict)>1:
                    name = '[' + record['company_id'][1] + '] ' + name
            res.append((record['id'], name))
        return res
