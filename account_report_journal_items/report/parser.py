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
        self.context=context
        self.filters=[]
        self.partner_filter=()       
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_wizard_params':self._get_wizard_params,
            'get_journal_moves':self._get_journal_moves,
            'get_journal_totals':self.get_journal_totals,
        })


    def _get_wizard_params(self,form_values):

        #parnter_filter
        if form_values['partner_id'] :
            #partner_id=form_values['partner_id']
            self.partner_filter=(form_values['partner_id'])

        #filters
        if form_values['date_from'] :
            date_storage_from=form_values['date_from']
            filter=("date",">=",date_storage_from)
            self.filters.append(filter)
        if form_values['date_to'] :
            date_storage_to=form_values['date_to']
            filter=("date","<=",date_storage_to)
            self.filters.append(filter)
        if form_values['account_id'] :
            date_storage_account=form_values['account_id']
            filter=("account_id","=",date_storage_account[0])
            self.filters.append(filter)

    def _get_journal_moves(self):

        journal_model=self.localcontext['data']['model']
        report_obj=self.pool.get(journal_model)
        line_ids=report_obj.search(self.cr,self.uid,self.filters)
        report_lines=report_obj.browse(self.cr,self.uid,line_ids)
        filter_line=[]
        if self.partner_filter :
            for line in report_lines:
                if line['move_id']['partner_id']['id'] == self.partner_filter :
                    filter_line.append(line)
            report_lines=filter_line
        return report_lines
    
    def get_journal_totals(self,positive=True):

        report_lines=self._get_journal_moves()
        plus=0
        minus=0
        for line in report_lines:
            if line['amount']>=0 :
                plus+=line['amount']
            else:
                minus+=line['amount']
        if positive :
            value=plus
        else:
            value=minus
        return value

       


