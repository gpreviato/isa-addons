# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 ISA s.r.l. (<http://www.isa.it>).
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

from osv import fields, osv
from tools.translate import _

class task_category(osv.osv):
    _description = 'Category of task'
    _name = 'project.task.category'
    _rec_name = 'code'
    
    _columns = {
        'name': fields.char('Description', size=80, required=True, select=True),
        'code': fields.char('Code', size=2, required=True, select=True),
        'ticket_required':fields.boolean('Ticket Required'),
    }
    
    _order = 'name'
        
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for item in self.browse(cr, uid, ids, context=context):
            item_desc = item.code and item.code + ' - ' or ''
            item_desc += item.name
            res.append((item.id,item_desc))
        return res

task_category()

class project_task(osv.osv):
    _inherit = 'project.task'

    def _hours_billing_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("SELECT task_id, COALESCE(SUM(billable_hours),0) FROM project_task_work WHERE task_id IN %s GROUP BY task_id",(tuple(ids),))
        hours = dict(cr.fetchall())
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = hours.get(task.id, 0.0)
        return res   

    def _get_project_task(self, cr, uid, ids, context=None):
        result = {}
        for work in self.pool.get('project.task.work').browse(cr, uid, ids, context=context):
            if work.task_id: result[work.task_id.id] = True
        return result.keys()

    _columns = {
        'category_id': fields.many2one('project.task.category', 'Category', ondelete="cascade",required=True),
        'ticket_reference':fields.char('Ticket reference', size=15, required=False),
        'need_ticket':fields.boolean(),
        'isa_billing_hours': fields.function(_hours_billing_get, method=True, string='Billable Hours',type='float' ,
            store = {
                'project.task': (lambda self, cr, uid, ids, c={}: ids, ['work_ids', 'isa_billing_hours'], 10),
                'project.task.work': (_get_project_task, ['billable_hours'], 10),
            }),
        'billing_as400_date':fields.datetime('Billing Date'),
        'billing_as400': fields.boolean('Transfer as400'),
        
    }
    def onchange_project(self, cr, uid, id, project_id):
        if not project_id:
            return {}
        data = self.pool.get('project.project').browse(cr, uid, [project_id])
        if data and data[0].parent_id.partner_id:
            partner_id=data and data[0].parent_id.partner_id
        else:
            partner_id=data and data[0].partner_id
        if partner_id:
            return {'value':{'partner_id':partner_id.id}}
        return {}
    

    def onchange_category(self, cr, uid, id, category_id):
        
        if not category_id:
            return {}
        #import pdb; pdb.set_trace()
        data = self.pool.get('project.task.category').browse(cr, uid, [category_id])
        result = {
                'need_ticket': False,
            }    
        if data and data[0].ticket_required == True:
            result = {
                'need_ticket': True,
            }    
        return {'value': result}


    def action_close(self, cr, uid, ids, context=None):
     #controlli per chiusura dell'attività
        values=self.read(cr,uid,ids)
        #HelpBoard - ticket da assegnare
        #se non è stato modificato l'user_id ed è stato lasciato Help_board,non permettere la chiusura
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [values[0]['user_id'][0]],['login'])
        if user[0]['login']== 'helpboard' :
            raise osv.except_osv(_('Error !'), _('You cannot close an activity with responsible HelpBoard.'))
            return False

        return super(project_task, self).action_close(cr, uid, ids, context)

    def do_open(self, cr, uid, ids, *args):
     #controlli per l'apertura dell'attività
        values=self.read(cr,uid,ids)
        #HelpBoard - ticket da assegnare
        #se non è stato modificato l'user_id ed è stato lasciato Help_board,non permettere la chiusura
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [values[0]['user_id'][0]],['login'])
        if user[0]['login']== 'helpboard' :
            raise osv.except_osv(_('Error !'), _('You cannot open an activity with responsible HelpBoard.'))
            return False
        return super(project_task, self).do_open(cr, uid, ids, args)


            
project_task()

