# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ISA s.r.l. (<http://www.isa.it>).
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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, orm
from openerp.tools.translate import _


class wizard_exporter_statements(orm.TransientModel):
    _name = 'wizard.exporter.statements'
    _columns = {
        'partner_id': fields.many2one('res.partner',
                                      'Partner'),
        'exporter_id': fields.many2one('account.exporter.statements',
                                       'Exporter Statements')
        
    }

    def print_exporter(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
        datas = {
             'ids': [],
             'model': 'account.exporter.statements',
             'form': self.read(cr, uid, ids)[0]
        }
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'exporter_statement_report',
            'datas':datas,
        }
