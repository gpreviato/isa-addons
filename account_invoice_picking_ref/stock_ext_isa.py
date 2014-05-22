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

class stock_picking_ext_isa(osv.osv):
    _inherit = 'stock.picking'
    
    def action_invoice_create(self, cr, uid, ids, journal_id=False,
            group=False, type='out_invoice', context=None):

        #import pdb; pdb.set_trace()
        picking_obj = self.pool.get('stock.picking')
        invoice_line_obj = self.pool.get('account.invoice.line')
        
        result = super(stock_picking_ext_isa, self).action_invoice_create(cr, uid,
                ids, journal_id=journal_id, group=group, type=type,
                context=context)
        
        #import pdb; pdb.set_trace()
        picking_ids = result.keys()
        for picking_id in picking_ids:
            pickings=picking_obj.browse(cr,uid,[picking_id])
            for picking in pickings:
                line_ids=invoice_line_obj.search(cr,uid,[('invoice_id', '=', result[picking_id]),('origin','like',picking.name)])
                invoice_line_obj.write(cr,uid,line_ids,{'document_reference_id':picking_id})
        return result
        
stock_picking_ext_isa()
            
