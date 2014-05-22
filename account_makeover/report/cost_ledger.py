# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import os
from openerp.report import report_sxw
from openerp.addons.account.project.report.cost_ledger import account_analytic_cost_ledger


class account_analytic_cost_ledger_makeover(account_analytic_cost_ledger):
    def __init__(self, cr, uid, name, context):
        super(account_analytic_cost_ledger_makeover, self).__init__(cr, uid, name, context=context)

    def _lines_a(self, general_account, account, date1, date2):
        self.cr.execute("SELECT aal.name AS name, aal.code AS code, aal.amount AS balance, aal.date AS date, aal.ref AS ref, aaj.code AS cj \
                FROM account_analytic_line AS aal, account_analytic_journal AS aaj \
                WHERE (aal.general_account_id=%s) AND (aal.account_id IN %s) AND (aal.date>=%s) AND (aal.date<=%s) \
                AND (aal.journal_id=aaj.id) \
                ORDER BY aal.date, aaj.code, aal.code", (general_account['id'], super(account_analytic_cost_ledger_makeover, self)._get_children([account]), date1, date2))
        res = self.cr.dictfetchall()
        for r in res:
            r['debit'] = r['balance'] if r['balance'] > 0 else 0.0
            r['credit'] = -r['balance'] if r['balance'] < 0 else 0.0
        return res

# remove previous report service :
from openerp.netsvc import Service
del Service._services['report.account.analytic.account.cost_ledger'] 

report_sxw.report_sxw('report.account.analytic.account.cost_ledger', 'account.analytic.account',
                      os.path.dirname(os.path.realpath(__file__)) + '/cost_ledger.rml',
                      parser=account_analytic_cost_ledger_makeover, header="internal")
