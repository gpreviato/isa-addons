# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 ISA srl (<http://www.isa.it>)
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

from openerp.report import report_sxw
from openerp.tools.translate import _
from openerp import pooler
import os
from datetime import datetime

from openerp.addons.account_financial_report_webkit.report.common_partner_reports import CommonPartnersReportHeaderWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser


class account_due_list_report_ext_isa(report_sxw.rml_parse, CommonPartnersReportHeaderWebkit):
    _name = 'account.due.list.report.ext.isa'

    def __init__(self, cursor, uid, name, context):
        self.cr = cursor
        self.uid = uid

        self.context = context
        super(account_due_list_report_ext_isa, self).__init__(cursor, uid, name, context)

        company = self.pool.get('account.due.list.report').browse(self.cr, self.uid, self.parents['active_id']).company_id
        self.filters = [('date_maturity', '!=', False),
                        ('reconcile_id', '=', False),('company_id','=',company.id)]
        
        header_report_name = ' - '.join((_('SCADENZARIO'), company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'cr': cursor,
            'uid': uid,
            'report_name': _('Scadenzario'),
            'get_wizard_params':self.get_wizard_params,
            'get_move_line':self._get_move_line,
            'get_reconcile_name':self.get_reconcile_name,
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
        })

    def get_wizard_params(self, date_from, date_to, partner):
        if date_from :
            f = ("date_maturity", ">=", date_from)
            self.filters.append(f)
        if date_to :
            t = ("date_maturity", "<=", date_to)
            self.filters.append(t)
        if partner :
            p = ("partner_id", "=", partner)
            self.filters.append(p)
        
        domain = ['|', '&', ('account_id.type', '=', 'payable'), ('debit', '=', 0), '&', ('account_id.type', '=', 'receivable'), ('credit', '=', 0)]
        for i in domain:
            self.filters.append(i)
    
    def _get_move_line(self):
        hrs = pooler.get_pool(self.cr.dbname).get('account.move.line')
        hrs_list = hrs.search(self.cr, self.uid, self.filters)
        move_lines = hrs.browse(self.cr, self.uid, hrs_list)
        return move_lines
    
    def get_reconcile_name(self, reconcile_id):
        reconcile_description = ''
        if reconcile_id:
            acc = pooler.get_pool(self.cr.dbname).get('account.move.reconcile')
            acc_list = acc.browse(self.cr, self.uid, reconcile_id)
            reconcile_description = acc_list.name_get()[0][1]
            
        return reconcile_description
        
HeaderFooterTextWebKitParser('report.due_list_pdf',
                             'account.move.line',
                             os.path.dirname(os.path.realpath(__file__)) + 
                                              '/template_due_list.mako',
                             parser=account_due_list_report_ext_isa)
