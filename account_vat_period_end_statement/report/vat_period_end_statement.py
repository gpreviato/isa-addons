# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
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

import time
from report import report_sxw

class print_vat_period_end_statement(report_sxw.rml_parse):
    _name = 'parser.vat.period.end.statement'

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(print_vat_period_end_statement, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {
            'time': time,
        })
        self.context = context

report_sxw.report_sxw('report.account.print.vat.period.end.statement',
                      'account.vat.period.end.statement',
                      'addons/account_vat_period_end_statement/report/vat_period_end_statement.mako',
                      parser=print_vat_period_end_statement)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
