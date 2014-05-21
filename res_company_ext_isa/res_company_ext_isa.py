# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

from osv import fields, osv
from tools.translate import _

class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'closed_days': fields.one2many('res.company.closed.day', 'company_id', 'Closed days', help="Identify the days of the week when the company closes"),
        'festivities': fields.one2many('res.company.festivity', 'company_id', 'Festivities', help="Indicate the days of the festivities"),
    }
    _defaults = {}

res_company()

class res_company_festivity(osv.osv):
    _name = 'res.company.festivity'
    _description = 'Day of festivity'
   
    _columns = {
        'name': fields.char('Name', size=80, required=True),
        'company_id': fields.many2one('res.company', 'Company Reference', required=True, ondelete="cascade", select=2),
        'year': fields.integer('Year'),
        'month': fields.integer('Month'),
        'day': fields.integer('Day'),
    }
    
    _defaults = {
        'company_id': lambda self, cr, uid, context: uid
    }
       
    _order = 'year desc'
    _order = 'month'
    _order = 'day'

res_company_festivity()

class res_company_closed_day(osv.osv):
    _name = 'res.company.closed.day'
    _description = 'Closed days'
    _rec_name = 'day'
    
    _columns = {
    #modificato l'intero in riferimento ai giorni per eliminare lo 0 del monday
        'day': fields.selection([(1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'),(7,'Sunday')], 'Day of the week', required=False),
        'company_id': fields.many2one('res.company', 'Company Reference', required=True, ondelete="cascade", select=2),
        'hours': fields.float('Number of hours', digits=(4,2), required=False),
    }
    
    _defaults = {
        'company_id': lambda self, cr, uid, context: uid
    }
       
    _order = 'day'

res_company_closed_day()



