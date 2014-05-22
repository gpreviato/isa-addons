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

import netsvc
import pooler
from osv import fields, osv, orm
from tools.translate import _

class account_invoice_cancel_ext_isa(osv.osv):
    _inherit = 'account.invoice'    
    
    # removed control over the internal_number    
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        #invoices = self.read(cr, uid, ids, ['state','internal_number'], context=context)    
        invoices = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in invoices:
            #if t['state'] in ('draft', 'cancel') and t['internal_number']== False:
            if t['state'] in ('draft', 'cancel'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid action !'), _('You can not delete an invoice which is open or paid. We suggest you to refund it instead.'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
    
account_invoice_cancel_ext_isa()
