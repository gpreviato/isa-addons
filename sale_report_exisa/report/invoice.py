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
        
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_ddt':self.get_ddt,
        })
    
    def get_ddt(self,origin):
        #import pdb;pdb.set_trace()
        result=False
        picking_obj=pooler.get_pool(self.cr.dbname).get('stock.picking')
        #import pdb;pdb.set_trace()
        if origin:
            picking_ids=picking_obj.search(self.cr,self.uid,[("name","=",origin)])
            if len(picking_ids)!=0:
                picking=picking_obj.browse(self.cr, self.uid, picking_ids)[0]
                if picking.ddt_number:
                    result="rif. %s del %s" % (picking.ddt_number,datetime.strptime(picking.ddt_date,'%Y-%m-%d').strftime('%d/%m/%Y'))
        return result
