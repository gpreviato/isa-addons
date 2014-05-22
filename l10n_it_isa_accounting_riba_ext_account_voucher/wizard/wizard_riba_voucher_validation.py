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
from osv import fields,osv
from tools.translate import _
import pooler



class wizard_riba_voucher_validation(osv.osv_memory):
    _name = 'riba_wizard_voucher_validation'
    _description = 'Voucher Validation from Riba'

    def validate_voucher(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        account_voucher = pooler.get_pool(cr.dbname).get('account.voucher')
        voucher_ids=self.check_vooucher_is_riba(cr, uid, context['active_ids'])  
        step1=account_voucher.proforma_voucher(cr, uid, voucher_ids , context)
      
        return {'type': 'ir.actions.act_window_close'}

    #Metodo che implementa il controllo deli voucher che si riferiscono alle riba
    def check_vooucher_is_riba(self, cr, uid, voucher_ids):
        return voucher_ids


    

wizard_riba_voucher_validation()



