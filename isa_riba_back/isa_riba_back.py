# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
from osv import osv, fields
import netsvc
from tools.translate import _

class riba_distinta(osv.osv):
    _inherit = 'riba.distinta'
    
    _columns = {
        'draftable': fields.boolean('draftable'),
    }
    
    _default = {
        'draftable': False,
    }

    def action_revert_done(self, cr, uid, ids, *args):
        #import pdb;pdb.set_trace()        

        if not len(ids):
            return False
        not_paid=True
       
        for distinta in self.browse(cr, uid, ids):

            if not distinta.draftable:
                raise osv.except_osv(_('Attention!'), _("If you want back to draft, you mast set 'allow back in draft'"))

            #record of account_move to set draft - always
            account_move_ids = []
            #record of reconsile -always
            account_move_line_ids = []

            #record of payment for state accredited
            payment_line_ids= []
            
            #record of unsolved for state unsolved
            unsolved_line_ids=[]                
            if distinta.accreditation_move_id.id :
                payment_line_ids.append(distinta.accreditation_move_id.id)

            for distinta_line in distinta.line_ids:
                if distinta_line.state == 'paid':
                    not_paid=False
                if distinta_line.acceptance_move_id.id:
                    account_move_ids.append(distinta_line.acceptance_move_id.id)
                if distinta_line.unsolved_move_id.id:
                    unsolved_line_ids.append(distinta_line.unsolved_move_id.id)
                for distinta_move_line in distinta_line.move_line_ids:
                    account_move_line_ids.append(distinta_move_line.move_line_id.id)

            if not_paid:
                self._account_move_unreconcile(cr, uid,account_move_line_ids)
                self._account_move_drowed(cr, uid,account_move_ids)
                if len(payment_line_ids):
                    self._account_move_drowed(cr, uid,payment_line_ids)
                if len(unsolved_line_ids):
                    self._account_move_drowed(cr, uid,unsolved_line_ids)
                self._back_to_draft(cr, uid, ids, *args)            
            else:
                raise osv.except_osv(_('Attention!'), _("In this distinta there is at least a riba paid.It's not possible back to draft!"))

        return True






# revert from ACCEPTED
    def action_revert_accepted(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        for distinta in self.browse(cr, uid, ids):
            account_move_line_ids = []
            account_move_ids = []
            for distinta_line in distinta.line_ids:
                account_move_ids.append(distinta_line.acceptance_move_id.id)
                for distinta_move_line in distinta_line.move_line_ids:
                    account_move_line_ids.append(distinta_move_line.move_line_id.id)

        self._account_move_unreconcile(cr, uid,account_move_line_ids)
        self._account_move_drowed(cr, uid,account_move_ids)

        return True
# revert from ACCREDITED
    def action_revert_accredited(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        for distinta in self.browse(cr, uid, ids):
            account_move_line_ids = []
            account_move_ids = []
            #pagamenti per stato accreditato
            payment_line_ids= []
            payment_line_ids.append(distinta.accreditation_move_id.id)
            for distinta_line in distinta.line_ids:
                account_move_ids.append(distinta_line.acceptance_move_id.id)
                for distinta_move_line in distinta_line.move_line_ids:
                    account_move_line_ids.append(distinta_move_line.move_line_id.id)
        self._account_move_unreconcile(cr, uid,account_move_line_ids)
        self._account_move_drowed(cr, uid,account_move_ids)
        #accreditamento in stato draft
        self._account_move_drowed(cr, uid,payment_line_ids)

        return True

# revert from UNSOLVED
    def action_revert_unsolved(self, cr, uid, ids, *args):
        if not len(ids):
            return False
        for distinta in self.browse(cr, uid, ids):
            account_move_line_ids = []
            account_move_ids = []
            #pagamenti per stato accreditato
            payment_line_ids= []
            #movimento per stato insoluto
            unsolved_line_ids=[]                
            payment_line_ids.append(distinta.accreditation_move_id.id)
            #distinta.state
            for distinta_line in distinta.line_ids:
                #distinta_line.state
                account_move_ids.append(distinta_line.acceptance_move_id.id)
                unsolved_line_ids.append(distinta_line.unsolved_move_id.id)
                for distinta_move_line in distinta_line.move_line_ids:
                    account_move_line_ids.append(distinta_move_line.move_line_id.id)
        self._account_move_unreconcile(cr, uid,account_move_line_ids)
        self._account_move_drowed(cr, uid,account_move_ids)
        self._account_move_drowed(cr, uid,payment_line_ids)
        self._account_move_drowed(cr, uid,unsolved_line_ids)
        return True


    #rimozione riconciliazione account_move_line: - da metodo account_unreconcile.trans_unrec  
    def _account_move_unreconcile(self, cr, uid, move_line_ids ):
        obj_move_line = self.pool.get('account.move.line')
        obj_move_line._remove_move_reconcile(cr, uid, move_line_ids )
        return True
    #impostazione draft pagamento- da metodo account.button_cancel
    def _account_move_drowed(self, cr, uid, move_ids ):
        obj_move = self.pool.get('account.move')
        obj_move.button_cancel(cr, uid, move_ids )
        return True
    #action cancel and cancel_draft ad setting riba_distinta_linse.state='draft'
    def _back_to_draft(self, cr, uid, ids, *args):
        #import pdb;pdb.set_trace()        
        self.riba_cancel(cr, uid, ids)
        self.action_cancel_draft(cr, uid, ids, *args)
        obj_distinta_line = self.pool.get('riba.distinta.line')
        for distinta in self.browse(cr, uid, ids):
            for distinta_line in distinta.line_ids:
                obj_distinta_line.write(cr, uid, distinta_line.id, {'state':'draft'})
            
        return True        

riba_distinta()
