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

from openerp.osv import orm


class account_voucher_ext_isa(orm.Model):

    _inherit = 'account.voucher'

    def button_proforma_voucher(self, cr, uid, ids, context=None):
        """
                Extends the button_proforma_voucher.
        """
        super(account_voucher_ext_isa,
              self).button_proforma_voucher(cr, uid, ids, context)
        
        acc_invoice_obj = self.pool.get('account.invoice')  
        acc_move_obj = self.pool.get('account.move')        
            
        for vid in ids:
            # leggere il move_id di account_voucher
            # cercare il record di account_move che ha id = move_id di
            #    account_voucher
            # cercare il record di account invoice che ha move_id = id di
            #    account move         
             
            record_fields = self.read(cr, uid, [vid], fields=None)[0]
            voucher_move_id = record_fields['move_id'][0]            
                        
            acc_move_id = acc_move_obj.search(cr, uid,
                                          [('id', '=', voucher_move_id), ],
                                          offset=0, limit=None, order=None,
                                          context=None, count=False)
            record_fields_move = acc_move_obj.read(cr, uid,
                                                   [acc_move_id[0] - 1],
                                                   fields=None)[0]
            name_acc_move = record_fields_move['name']          
            
            acc_invoice_id = acc_invoice_obj.search(cr, uid,
                                                    [('number', '=', name_acc_move)], offset=0,
                                                    limit=None, order=None, context=None,
                                                    count=False)

            record_fields = acc_invoice_obj.read(cr, uid, [acc_invoice_id[0]],
                                                 fields=None)[0]
            fiscal_position = record_fields['fiscal_position']
            if fiscal_position:
                if acc_invoice_obj.check_intracee(cr, uid, fiscal_position[0]):
                    acc_invoice_obj.write(cr, uid,
                                          [acc_invoice_id[0]], {'state': 'paid', })

        return {'type': 'ir.actions.act_window_close'}
