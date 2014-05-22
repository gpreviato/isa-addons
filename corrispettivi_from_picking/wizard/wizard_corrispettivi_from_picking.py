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

from openerp.osv import fields, osv
from tools.translate import _

class stock_corrispettivo_onshipping(osv.osv_memory):

    _inherit = "stock.invoice.onshipping"
    
    def _get_journal_id(self, cr, uid, context=None):
        
        #import pdb;pdb.set_trace()
        journal_obj = self.pool.get('account.journal')
        
        if not context.has_key('invoice_type') or context['invoice_type']!='corrispettivo':
            vals = super(stock_corrispettivo_onshipping, self)._get_journal_id(cr, uid, context)
            journal_acc_ids = journal_obj.search(cr, uid, [('corrispettivi', '=',True)])
            #import pdb;pdb.set_trace()
            tmp_vals=[]
            for j in vals:
                if j[0] not in journal_acc_ids: 
                    tmp_vals.append(j)
            vals=tmp_vals
        else:
            if context is None:
                context = {}

            model = context.get('active_model')
            if not model or model != 'stock.picking':
                return []

            model_pool = self.pool.get(model)
            res_ids = context and context.get('active_ids', [])
            vals = []
            browse_picking = model_pool.browse(cr, uid, res_ids, context=context)
            
            for pick in browse_picking:
                if not pick.move_lines:
                    continue
                src_usage = pick.move_lines[0].location_id.usage
                dest_usage = pick.move_lines[0].location_dest_id.usage
                type = pick.type
                   
                if type != 'out' and dest_usage != 'customer':
                    raise Exception(_("Warning: you can create corrispettivi only for out delivery to customers!"))
                #import pdb; pdb.set_trace()
                value = journal_obj.search(cr, uid, [('corrispettivi', '=',True)])
                for jr_type in journal_obj.browse(cr, uid, value, context=context):
                    t1 = jr_type.id,jr_type.name
                    if t1 not in vals:
                        vals.append(t1)
            if not vals:
                raise osv.except_osv(_('Warning !'), _('Either there are no moves linked to the picking or Accounting Journals are misconfigured!'))
        #import pdb; pdb.set_trace()
        return vals
    
    _columns = {
        'journal_id': fields.selection(_get_journal_id, 'Destination Journal',required=True),
    }

stock_corrispettivo_onshipping()

