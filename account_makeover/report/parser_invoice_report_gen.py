# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 ISA s.r.l. (<http://www.isa.it>).
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
from openerp.report import report_sxw
from openerp import pooler
import os

from webkit_parser_header_fix import HeaderFooterTextWebKitParser

class parser_invoice_report_gen(report_sxw.rml_parse):
    _name = 'account.invoice.report.gen.isa'

    def __init__(self, cr, uid, name, context=None):
        self.cr = cr
        self.uid = uid
        if context is None:
            context = {}
        super(parser_invoice_report_gen,
              self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_move_line':self._get_move_line,
            'get_order_invoice_line': self._get_order_invoice_line,
            'has_picking': self._has_picking,
            'count_lines': self._count_lines,
        })
        self.context = context

    def _get_move_line(self, move_id):
        hrs = pooler.get_pool(self.cr.dbname).get('account.move.line')
        hrs_list = hrs.search(self.cr, self.uid,
                              [('move_id', '=', move_id),
                               ('date_maturity', '!=', False), ],
                              order='date_maturity')
        move_lines = hrs.browse(self.cr, self.uid, hrs_list)
        return move_lines

    def _get_order_invoice_line(self, invoice_id, limit_page, offset_page):
        invoice_obj = pooler.get_pool(self.cr.dbname).get('account.invoice')
        invoice_data = invoice_obj.browse(self.cr, self.uid, invoice_id)
        invoice_lines = []
        if invoice_data and invoice_data.invoice_line:
            hrs_list = []
            hrs = pooler.get_pool(self.cr.dbname).get('account.invoice.line')
            hrs_list = hrs.search(self.cr, self.uid,
                                  [('invoice_id', '=', invoice_id), ],
                                  limit=limit_page,
                                  offset=offset_page)
            invoice_lines = hrs.browse(self.cr, self.uid, hrs_list)
        return invoice_lines

    def _has_picking(self, invoice_id):
        invoice_obj = pooler.get_pool(self.cr.dbname).get('account.invoice')
        invoice_data = invoice_obj.browse(self.cr, self.uid, invoice_id)
        if invoice_data and invoice_data.invoice_line:
            if not hasattr(invoice_data.invoice_line[0],'document_reference_id'):
                return False
            t_ddt = invoice_data.invoice_line[0].document_reference_id
            if (t_ddt and t_ddt.ddt_number):
                return True
        return False

    def _count_lines(self, invoice_id):
        num_lines = 0
        invoice_obj = pooler.get_pool(self.cr.dbname).get('account.invoice')
        invoice_data = invoice_obj.browse(self.cr, self.uid, invoice_id)
        if invoice_data and invoice_data.invoice_line:
            for _ in invoice_data.invoice_line:
                num_lines = num_lines +1
        return num_lines

HeaderFooterTextWebKitParser('report.fattura_gen_report',
                             'account.invoice',
                             os.path.dirname(os.path.realpath(__file__)) + 
                                                      '/invoice_gen.mako',
                             parser=parser_invoice_report_gen)
