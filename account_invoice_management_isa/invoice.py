# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
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
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import netsvc
from osv import fields, osv

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        #'internal_number':fields.many2one('account.invoice.cancel.isa', 'Invoice number',readonly=True, states={'draft':[('readonly',False)]}), 
        'internal_number_isa':fields.many2one('account.invoice.cancel.isa', 'Invoice number',readonly=True, states={'draft':[('readonly',False)]}),
        'internal_number_isa_visible':fields.related('journal_id', 'update_force_number_isa', type="boolean", relation="account.journal",store=False),
        'internal_number_visible':fields.related('journal_id', 'update_force_number', type="boolean", relation="account.journal",store=False),
        }  
    
#salvataggio in tabella isa_cancel dal metodo chiamato dal tasto annulla 
    def action_cancel(self, cr, uid, ids, *args):
        account_cancel_obj = self.pool.get('account.invoice.cancel.isa')
        for invoice in self.browse(cr, uid,ids ):
            if invoice['number'] :
                isset_invoice = account_cancel_obj.search(cr, uid,[('number', '=', invoice['number'])])
                if not isset_invoice:
                    account_cancel=account_cancel_obj.create(cr,uid,
                                                             {'number': str(invoice['number']),
                                                              'journal_id': invoice['journal_id']['id'],
                                                              } )            
        
        return super(account_invoice, self).action_cancel(cr, uid, ids, *args)
            
    #copiatura valore internal_number_isa(che potrebbe essere store=false) in internal number
    # salvataggio ed eventuale cancellazione record da tabella cancel_isa
    #pulsante invoice_open che agisce sul workflow.
    def invoice_open(self, cr, uid, ids, *args):
        #import pdb;pdb.set_trace()
        values=self.read(cr,uid,ids)
        invoice_cancel_isa=False
        #se esiste l'internal number isa sovreascrive l'internal number 
        if values[0]['internal_number_isa']:
            invoice_cancel_isa=self.write(cr,uid,ids,{'internal_number':str(values[0]['internal_number_isa'][1]),})        
            if invoice_cancel_isa :
                account_cancel_obj = self.pool.get('account.invoice.cancel.isa')
                account_cancel_id = account_cancel_obj.search(cr, uid,[('number', '=', str(values[0]['internal_number_isa'][1]))])
                account_cancel_obj.unlink(cr, uid, account_cancel_id)
        #se esiste l'internal number,controlla che non sia nella tabella account_invoice_cancel_isa.Se c'è cancellalo
        else :
            if values[0]['internal_number']:
                account_cancel_obj = self.pool.get('account.invoice.cancel.isa')
                account_cancel_id = account_cancel_obj.search(cr, uid,[('number', '=', str(values[0]['internal_number']))])
                account_cancel_obj.unlink(cr, uid, account_cancel_id)

        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            wf_service.trg_validate(uid, 'account.invoice', id, 'invoice_open', cr)
        return True
    
account_invoice()
