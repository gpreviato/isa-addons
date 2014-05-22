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
#    _name = 'account.account'
    _inherit = 'account.account'

    def onchange_parent_id(self, cr, uid, ids, parent_id):

        if not parent_id:
            return {}

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

            str_pad = str_pad_res[0]['code_digits']

            max_code = max_code.ljust(str_pad, '0')
            max_code = str(int(max_code) +1)
            max_code = max_code.rjust(str_pad, '0');
            
            res = {'value':{'code': max_code }}

        return res


    _defaults = {
        'code': '',
    }

account_accounts_code_digits_ext_isa()


