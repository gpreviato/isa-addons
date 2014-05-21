# -*- coding: utf-8 -*-
###############################################################################
#
##############################################################################

import time
import pooler
from osv import osv, fields

class hr_summary_odt_bymonth(osv.osv_memory):
    _name = 'hr.employee.report.summary_odt.month'
    _description = 'Print Monthly Holidays Report'
    _columns = {
        'month': fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 'Month', required=True),
        'year': fields.integer('Year', required=True)
    }
    _defaults = {
         'month': lambda *a: time.gmtime()[1],
         'year': lambda *a: time.gmtime()[0],
    }

    def print_report(self, cr, uid, ids, context={}):
        #import pdb; pdb.set_trace()
        datas = {
             'ids': [],
             'model': 'hr.employee',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'summary_odt',
            'datas':datas,
        }

hr_summary_odt_bymonth()

class hr_summary_self_odt_bymonth(osv.osv_memory):
    _name = 'hr.employee.report.summary_self_odt.month'
    _description = 'Print Monthly Holidays Report'
    _columns = {
        'month': fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 'Month', required=True),
        'year': fields.integer('Year', required=True)
    }
    _defaults = {
         'month': lambda *a: time.gmtime()[1],
         'year': lambda *a: time.gmtime()[0],
    }

    def print_report(self, cr, uid, ids, context={}):
        
        datas = {
             'ids': [],
             'model': 'hr.employee',
             'form': self.read(cr, uid, ids)[0]
        }
        #import pdb; pdb.set_trace()
        res_ids=pooler.get_pool(cr.dbname).get('resource.resource').search(cr,uid,[("user_id","=",uid)])
        emp_ids=pooler.get_pool(cr.dbname).get('hr.employee').search(cr,uid,[("resource_id","in",res_ids)])
        context['active_ids']=emp_ids
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'summary_odt',
            'datas':datas,
            'context':context,
        }

hr_summary_self_odt_bymonth()
