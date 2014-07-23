# -*- coding: utf-8 -*-
###############################################################################
#
##############################################################################

from openerp.osv import orm, fields

class due_list(orm.TransientModel):
    _name = 'account.due.list.report'
    _description = 'Print Account Due List Report'
    _columns = {
        'company_id': fields.many2one('res.company', 
                                      'Company', 
                                      required=True), 
        'date_maturity_from': fields.date('Due Date From'),
        'date_maturity_to': fields.date('Due Date To'),
        'partner_wizard': fields.many2one('res.partner', 'Partner')
    }
    _defaults = {
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, context=c),        
    }

    def print_report_pdf(self, cr, uid, ids, context=None):
        datas = {
             'ids': [],
             'model': 'account.move.line',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'due_list_pdf',
            'datas':datas,
        }
