# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 OpenERP Italian Community (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw
import pooler
from datetime import datetime

class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        self.cr=cr
        self.uid=uid
        
        self.lang='it_IT.utf8'
        
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'sale_order_lines':self.sale_order_lines,
        })
        

        #~ ids = pooler.get_pool(self.cr.dbname).get('account.invoice.line').search(self.cr, self.uid, [('invoice_id', '=', invoice_id)])        
        #~ for id in range(0, len(ids)):
            #~ info = pooler.get_pool(self.cr.dbname).get('account.invoice.line').browse(self.cr, self.uid, ids[id])
            #~ list_in_seq[info] = info.sequence
        #~ i = 1
        #~ j = 0
        #~ final=sorted(list_in_seq.items(), lambda x, y: cmp(x[1], y[1]))
        #~ invoice_list = [x[0] for x in final]
            
    def sale_order_lines(self, sale_order):
        result = []
        sub_total = {}
        order_lines = []
        res = {}
        obj_order_line = self.pool.get('sale.order.line')
        
        list_in_seq = {}
        ids = obj_order_line.search(self.cr, self.uid, [('order_id', '=', sale_order.id)])
        for id in range(0, len(ids)):
            info = obj_order_line.browse(self.cr, self.uid, ids[id])
            list_in_seq[info] = info.sequence
        i = 1
        j = 0
        final=sorted(list_in_seq.items(), lambda x, y: cmp(x[1], y[1]))
        invoice_list = [x[0] for x in final]
        
        return invoice_list


        #~ ids = obj_order_line.search(self.cr, self.uid, [('order_id', '=', sale_order.id)])
        #~ for id in range(0, len(ids)):
            #~ order = obj_order_line.browse(self.cr, self.uid, ids[id], self.localcontext.copy())
            #~ order_lines.append(order)
#~ 
        #~ i = 1
        #~ j = 0
        #~ sum_flag = {}
        #~ sum_flag[j] = -1
        #~ for entry in order_lines:
            #~ res = {}
#~ 
            #~ if entry.layout_type == 'article':
                #~ res['tax_id'] = ', '.join(map(lambda x: x.name, entry.tax_id)) or ''
                #~ res['name'] = entry.name
                #~ res['product_uom_qty'] = entry.product_uos and entry.product_uos_qty or entry.product_uom_qty or 0.00
                #~ res['product_uom'] = entry.product_uos and entry.product_uos.name or entry.product_uom.name
                #~ res['price_unit'] = entry.price_unit or 0.00
                #~ res['discount'] = entry.discount and entry.discount or 0.00
                #~ res['price_subtotal'] = entry.price_subtotal and entry.price_subtotal or 0.00
                #~ sub_total[i] = entry.price_subtotal and entry.price_subtotal
                #~ i = i + 1
                #~ res['note'] = entry.notes or ''
                #~ res['currency'] = sale_order.pricelist_id.currency_id.name
                #~ res['layout_type'] = entry.layout_type
            #~ else:
                #~ res['product_uom_qty'] = ''
                #~ res['price_unit'] = ''
                #~ res['discount'] = ''
                #~ res['tax_id'] = ''
                #~ res['layout_type'] = entry.layout_type
                #~ res['note'] = entry.notes or ''
                #~ res['product_uom'] = ''
#~ 
                #~ if entry.layout_type == 'subtotal':
                    #~ res['name'] = entry.name
                    #~ sum = 0
                    #~ sum_id = 0
                    #~ if sum_flag[j] == -1:
                        #~ temp = 1
                    #~ else:
                        #~ temp = sum_flag[j]
#~ 
                    #~ for sum_id in range(temp, len(sub_total)+1):
                        #~ sum += sub_total[sum_id]
                    #~ sum_flag[j+1] = sum_id +1
#~ 
                    #~ j = j + 1
                    #~ res['price_subtotal'] = sum
                    #~ res['currency'] = sale_order.pricelist_id.currency_id.name
                    #~ res['quantity'] = ''
                    #~ res['price_unit'] = ''
                    #~ res['discount'] = ''
                    #~ res['tax_id'] = ''
                    #~ res['product_uom'] = ''
                #~ elif entry.layout_type == 'title':
                    #~ res['name'] = entry.name
                    #~ res['price_subtotal'] = ''
                    #~ res['currency'] = ''
                #~ elif entry.layout_type == 'text':
                    #~ res['name'] = entry.name
                    #~ res['price_subtotal'] = ''
                    #~ res['currency'] = ''
                #~ elif entry.layout_type == 'line':
                    #~ res['product_uom_qty'] = '__________'
                    #~ res['price_unit'] = '______________'
                    #~ res['discount'] = '___________'
                    #~ res['tax_id'] = '_________________'
                    #~ res['product_uom'] = '_____'
                    #~ res['name'] = '_______________________________________'
                    #~ res['price_subtotal'] = '_________'
                    #~ res['currency'] = '_______'
                #~ elif entry.layout_type == 'break':
                    #~ res['layout_type'] = entry.layout_type
                    #~ res['name'] = entry.name
                    #~ res['price_subtotal'] = ''
                    #~ res['currency'] = ''
                #~ else:
                    #~ res['name'] = entry.name
                    #~ res['price_subtotal'] = ''
                    #~ res['currency'] = sale_order.pricelist_id.currency_id.name
#~ 
            #~ result.append(res)
            
        #~ return result
    
