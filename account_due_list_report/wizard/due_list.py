# -*- coding: utf-8 -*-
###############################################################################
#
##############################################################################

import time

from osv import osv, fields
from tools.translate import _

class due_list(osv.osv_memory):
    _name = 'account.due.list.report'
    _description = 'Print Account Due List Report'
    _columns = {
        'date_maturity_from': fields.date('Due Date From'),
        'date_maturity_to': fields.date('Due Date To'),
        'partner_wizard': fields.many2one('res.partner', 'Partner')
    }
   
    def print_report_ods(self, cr, uid, ids, context={}):
        datas = {
             'ids': [],
             'model': 'account.move.line',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'due_list_ods',
            'datas':datas,
        }

    def print_report_odt(self, cr, uid, ids, context={}):
        datas = {
             'ids': [],
             'model': 'account.move.line',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'due_list_odt',
            'datas':datas,
        }

due_list()
