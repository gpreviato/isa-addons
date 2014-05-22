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

from osv import osv, fields
from tools.translate import _
import decimal_precision as dp

class product_last_price(osv.osv):
    
    _inherit = 'product.product'
    _description = "Product extension for last price"
    
    def _last_purchase_price(self, cr, uid, ids, name, arg, context=None):
        
        if context.get('shop', False):
            cr.execute('select warehouse_id from sale_shop where id=%s', (int(context['shop']),))
            res2 = cr.fetchone()
            if res2:
                context['warehouse'] = res2[0]

        if context.get('warehouse', False):
            cr.execute('select lot_stock_id from stock_warehouse where id=%s', (int(context['warehouse']),))
            res2 = cr.fetchone()
            if res2:
                context['location'] = res2[0]

        if context.get('location', False):
            if type(context['location']) == type(1):
                location_ids = [context['location']]
            elif type(context['location']) in (type(''), type(u'')):
                location_ids = self.pool.get('stock.location').search(cr, uid, [('name','ilike',context['location'])], context=context)
            else:
                location_ids = context['location']
        else:
            location_ids = []
            wids = self.pool.get('stock.warehouse').search(cr, uid, [], context=context)
            for w in self.pool.get('stock.warehouse').browse(cr, uid, wids, context=context):
                location_ids.append(w.lot_stock_id.id)
        
        
        where = [tuple(location_ids),tuple(location_ids),tuple(ids)]
        query="""select id,price_unit 
            from stock_move
            where location_id NOT IN %s
            and location_dest_id IN %s
            and product_id IN %s
            and state IN ('confirmed', 'done')
            and price_unit is not null 
            order by id desc"""
        cr.execute(query , tuple(where))
        results = cr.fetchall()
        res={}.fromkeys(ids, 0.0)
        if results: 
            res[ids[0]]=results[0][1]
        #~ import pdb; pdb.set_trace()
        return res
    
    _columns = {
        'last_purchase_price':fields.function(_last_purchase_price, method=True, store=False, type='float', string='Last purchase price', digits_compute=dp.get_precision('Sale Price')),
    }
    
product_last_price()
