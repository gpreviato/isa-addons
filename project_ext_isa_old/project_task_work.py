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

class work_type(osv.osv):
    _description = 'Type of work'
    _name = 'project.task.work.type'
    
    _columns = {
        'name': fields.char('Description', size=80, required=True, select=True),
        'code': fields.char('Code', size=2, required=True),
    }
    
    
    _order = 'code'
        
work_type()

class project_task_work(osv.osv):
    _inherit = 'project.task.work'
    
    _columns = {
        'type_id': fields.many2one('project.task.work.type', 'Type of work', ondelete="cascade",required=True),
        'program':fields.char('Program', size=50, required=False), 
        'file':fields.char('File', size=50, required=False), 
        'field':fields.char('Field', size=50, required=False), 
        'ptf_code':fields.char('PTF code', size=50, required=False), 
        'description': fields.text('Description'),
        'billable_hours': fields.float('Billable hours'),
        'project_id': fields.related('task_id','project_id',type="many2one",relation="project.project",string='Project',store=False),
        'task': fields.related('task_id',type="many2one",relation="project.task",string='Activities',store=False),
        'not_billing': fields.boolean('Not Billing'),
    }
    def duplicate_work(self, cr, uid, id, default={}, context=None):
        #import pdb; pdb.set_trace()
        id=id[0]
        if context is None:
            context = {}
        res = super(project_task_work, self).copy(cr, uid, id, default, context)
        return res
    
    def create(self, cr, uid, vals, *args, **kwargs):
        if vals['not_billing']:
            vals['billable_hours']=0.00
        else :
            if not vals['billable_hours']:
                vals['billable_hours']=vals['hours']

        return super(project_task_work,self).create(cr, uid, vals, *args, **kwargs)

    def write(self, cr, uid, ids, vals, context=None):
        
        check_vals=self._check_billable_hours(cr, uid, ids, vals, context)
        return super(project_task_work,self).write(cr, uid, ids, check_vals, context)

    #a seconda del flag di not_billing. Il controllo non viene effettuato se il lavoro è di tipo
    #ZZ che serve per gestire il pregresso id=30    utilizzo l'id perchè da vals ho solo l'id

    def _check_billable_hours(self, cr, uid, ids, vals, context=None):
        #import pdb; pdb.set_trace()
        values=self.read(cr,uid,ids)
        if vals.has_key('type_id'):
            if vals['type_id']==30:
                return vals
        else :
            if values[0]['type_id'][0]==30:
                return vals
    
        for key,val in vals.iteritems():
            if key in values[0]:
                values[0][key]=val

        if values[0]['not_billing']:
            vals['billable_hours']=0.00
        else:
            vals['billable_hours']= values[0]['hours']
        return vals


project_task_work()

