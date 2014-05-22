# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2013 OpenERP Italian Community (<http://www.openerp-italia.org>). 
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
from openerp.report import report_sxw

class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):    
        self.context=context
        self.filters=[]
        self.total_credit = 0.0
        self.total_debit = 0.0
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_journal_moves':self._get_journal_moves,
            'get_journal_totals_credit':self._get_journal_totals_credit,
            'get_journal_totals_debit':self._get_journal_totals_debit,
            'get_journal_margins':self._get_journal_margins
        })


    def _get_journal_moves(self,form_values, selected_items):

        selected_items = tuple(selected_items)
        if len(selected_items) == 1 :
            selected_items = "("+str(selected_items[0])+")"
            
        query = "SELECT aa.name AS name, aa.code AS code \
                     ,aal.amount AS balance, pp.name AS partner \
                     ,aal.date AS date, aal.ref AS ref, aal.name AS desc \
                     ,aaa.name AS an_ac_name, aaj.name AS journal \
                FROM account_account aa \
                     inner join account_analytic_line aal on aal.general_account_id=aa.id \
                     inner join account_analytic_account aaa on aaa.id=aal.account_id \
                     left outer join account_move_line aml on aml.id=aal.move_id \
                     left outer join account_analytic_journal aaj on aaj.id=aal.journal_id \
                     left outer join res_partner pp on pp.id=aml.partner_id "
        query += "WHERE aal.account_id IN " + str(selected_items) + " "
                    
        if form_values['date_from']:
            query+="AND (aal.date>='"+form_values['date_from']+"') "
        
        if form_values['date_to']:
            query+="AND (aal.date<='"+form_values['date_to']+"') "

        query+=" ORDER BY aal.code"

        self.cr.execute(query)
        res = self.cr.dictfetchall()

        for r in res:
            if r['balance'] > 0:
                r['debit'] = r['balance']
                r['credit'] = 0.0
                self.total_debit += float(r['balance'])
            elif r['balance'] < 0:
                r['debit'] = 0.0
                r['credit'] = -r['balance']
                self.total_credit += float(r['balance'])
            else:
                r['debit'] = 0.0
                r['credit'] = 0.0
        return res

    
    def _get_journal_totals_credit(self):
        return self.total_credit

    def _get_journal_totals_debit(self):
        return self.total_debit
 
    def _get_journal_margins(self):
        return self.total_credit + self.total_debit




