# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import pooler
from report import report_sxw

class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):

        self.type_article=[]        
        self.type_subtotal=[]        
        self.type_title=[]
        self.type_text=[]
        self.type_line=[]
        self.type_break=[]
        self.cr=cr
        self.uid=uid
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_lines':self.get_line_type_by_orm,
            'printable':self.printable,
        })

    def get_line_type_by_orm(self,invoice_id):
        list_in_seq = {}
        article={}
        ids = pooler.get_pool(self.cr.dbname).get('account.invoice.line').search(self.cr, self.uid, [('invoice_id', '=', invoice_id)])        
        for id in range(0, len(ids)):
            info = pooler.get_pool(self.cr.dbname).get('account.invoice.line').browse(self.cr, self.uid, ids[id])
            list_in_seq[info] = info.sequence
        i = 1
        j = 0
        final=sorted(list_in_seq.items(), lambda x, y: cmp(x[1], y[1]))
        invoice_list = [x[0] for x in final]
        sum_flag = {}
        sum_flag[j] = -1
        for entry in invoice_list:
            #import pdb; pdb.set_trace()
            if entry.state == 'subtotal':
                self.type_subtotal.append(entry)
            if entry.state == 'title':
                #entry['quantity'] = ''
                self.type_title.append(entry)
            if entry.state == 'text':
                #entry['quantity'] = ''
                self.type_text.append(entry)
            if entry.state == 'line':
                #entry['quantity'] = ''
                self.type_line.append(entry)
            if entry.state == 'break':
                #entry['quantity'] = ''
                self.type_break.append(entry)
            if entry.state == 'article':
                self.type_article.append(entry)
        #self.invoice_list=invoice_list
        return invoice_list

    #elimina la quantità per il tipo template    
    def printable(self,num):
        if num>0:
            return True
        return False
    
     #TODO: fare una classe parser da estendere?

