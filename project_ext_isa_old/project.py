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

import time
from osv import fields, osv
from tools.translate import _
class project_category(osv.osv):
    _description = 'Category of project'
    _name = 'project.category'
    _rec_name = 'code'
    
    _columns = {
        'name': fields.char('Description', size=80, required=True, select=True),
        'code': fields.char('Code', size=2, required=True, select=True),
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

project_category()

class project__closinng_category(osv.osv):
    _description = 'Category of closing project'
    _name = 'project.closing_category'
    _rec_name = 'code'
    
    _columns = {
        'name': fields.char('Description', size=80, required=True, select=True),
        'code': fields.char('Code', size=2, required=True, select=True),
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

project__closinng_category()

class project(osv.osv):
    _inherit = 'project.project'

    def _get_billing_states(self, cr, uid, context=None):
        return ()

    def _hours_billing_project_get(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        cr.execute("SELECT project_id, COALESCE(SUM(isa_billing_hours),0) FROM project_task WHERE project_id IN %s GROUP BY project_id",(tuple(ids),))
        hours = dict(cr.fetchall())
        for task in self.browse(cr, uid, ids, context=context):
            res[task.id] = hours.get(task.id, 0.0)
        return res   

    def _get_isa_task(self, cr, uid, ids, context=None):
        result = {}
        for task in self.pool.get('project.task').browse(cr, uid, ids, context=context):
            if task.project_id: result[task.project_id.id] = True
        return result.keys()
  
    _columns = {
        'billing_state': fields.selection([('01', '01 - Not to be billed'),('02', '02 - To be billed'),('03', '03 - Billed')], 'State billing', select=True),
        'billing_month': fields.selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 'Month billing'),
        'billing_year': fields.integer('Year billing'),
        'category_id': fields.many2one('project.category', 'Category'),
        #'billing_hours_project':fields.float('Billing Hours'),
        'billing_hours_project': fields.function(_hours_billing_project_get, method=True,type='float' ,
            store = {
                'project.project': (lambda self, cr, uid, ids, c={}: ids, ['tasks'], 10),
                'project.task': (_get_isa_task, ['isa_billing_hours'], 10),
            }),

        #'hours_for_partner':fields.float('Hours worked for partners'),
        'hours_for_partner':fields.related('effective_hours',type="float", relation='project.project', string='Hours worked for partners', store=True, readonly=True),
        'close_description':fields.text('Close Description'),
        'closing_category_id': fields.many2one('project.closing_category', 'Causal Closure'),
        'billing_as400': fields.boolean('Transfer as400'),
        'included_package': fields.boolean('included package hours'),
        #'contract':fields.char('Contract', size=6 ),       
        'contract':fields.many2one('project.contract', 'Contract'),
        #'contract' : fields.function(_get_contract_id,type='many2one', method=True),
         #'contract_line':fields.char('Contract Line', size=6 ),
        'contract_line':fields.many2one('project.contract.line', 'Category Line'),
        'billing_as400_date':fields.datetime('Billing Date'),
        'contract_mod_date':fields.datetime('Contract Modify Date'),


    }
    
    _defaults = {
         #'billing_month': lambda *a: time.gmtime()[1],
         #'billing_year': lambda *a: time.gmtime()[0],
    }
            
    def onchange_billing_state(self, cr, uid, ids, newstate, context=None):
        #if newstate == "01":
        #    return {'value':{'billing_month': 0, 'billing_year': 0}}
        #act_month = time.gmtime()[1]
        #act_year = time.gmtime()[0]
        #return {'value':{'billing_month': act_month, 'billing_year': act_year}}
        return {}

#aggiunge data chiusura alla "chiusura" del progetto ed effettua i controlli
    def set_done(self, cr, uid, ids, context=None):
        
        #controlli per chiusura progetto       
        values=self.read(cr,uid,ids)

        #controllo stato attività collegate al progetto
        task=self._check_open_task(cr, uid, ids)

        #se è già stata assegnata data chiusura,la mantiene, altrimenti mette la data odierna,
        end_date=values[0]['date'] 
        if not end_date:
            end_date=time.strftime('%Y-%m-%d %H:%M:%S')

        #HelpBoard - ticket da assegnare
        #se non è stato modificato l'user_id ed è stato lasciato Help_board,non permettere la chiusura
        user_obj = self.pool.get('res.users')
        user = user_obj.read(cr, uid, [values[0]['user_id'][0]],['login'])
        if user[0]['login']== 'helpboard' :
            raise osv.except_osv(_('Error !'), _('You cannot close a project with projec manager HelpBoard.'))
            return False
        #se ore fatturate = 0 solo se tipologia è "da non fatturare"
        #import pdb;pdb.set_trace()
        if not values[0]['billing_state']:
            raise osv.except_osv(_('Error !'), _('You must select billing state.'))
        
        if values[0]['billing_state']!= '01' :
            if values[0]['billing_hours_project'] <= 0 :
                raise osv.except_osv(_('Error !'), _('You cannot close a project with billing hours not correct.'))
                return False

        #Se il nome del progetto inizia con HB_ il progetto si può chiudere solo se abbiamo valore per le note di chiusura
        if values[0]['name'].find('HR_',0,3) == 0 :
            if not (values[0]['closing_category_id'] and  values[0]['close_description']) :
                raise osv.except_osv(_('Error !'), _('You cannot close a project with name strting with "HR_" without closing informations.'))
                return False
        #import pdb;pdb.set_trace()
        #Se la categoria del progetto è "85 - Assistenza presso clienti" riga contratto è required
        if  values[0]['category_id'] and values[0]['category_id'][1].find('85',0,2) == 0 :
            if not values[0]['contract_line'] :
                raise osv.except_osv(_('Error !'), _('You cannot close a project with category "85 - Assistenza presso clienti" without select contract line'))
        task_obj = self.pool.get('project.task')
        task_ids = task_obj.search(cr, uid, [('project_id', 'in', ids), ('state', 'not in', ('cancelled', 'done'))])
        task_obj.write(cr, uid, task_ids, {'state': 'done', 'date_end':time.strftime('%Y-%m-%d %H:%M:%S'), 'remaining_hours': 0.0})
        self.write(cr, uid, ids, {'state':'close','date':end_date}, context=context)
        for (id, name) in self.name_get(cr, uid, ids):
            message = _("The project '%s' has been closed.") % name
            self.log(cr, uid, id, message)
        return True

    #controllo stato attività collegate progetto
    def _check_open_task (self, cr, uid, ids):
        #import pdb;pdb.set_trace()
        task_obj = self.pool.get('project.task')
        tasks_id = task_obj.search(cr, uid, [('project_id','=',ids[0])])
        tasks=task_obj.browse(cr, uid, tasks_id) 
        for task in tasks:
            if task.state not in ['cancelled', 'done']:
                raise osv.except_osv(_('Warning !'), _('Non si puo\' chiudere il progetto perche\' lo stato del lavoro "%s" non e\' "cancellato" o "terminato".' %task.name))
                raise osv.except_osv(_('Warning !'), _('You cannot close this project,because the project_task "%s" state is not "cancelled" or "done".' %task.name))
        return True



    def onchange_contract(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        #if newstate == "01":
        #    return {'value':{'billing_month': 0, 'billing_year': 0}}
        #act_day = time.gmtime()[2]
        #act_month = time.gmtime()[1]
        #act_year = time.gmtime()[0]
        act_date = time.strftime('%Y-%m-%d %H:%M:%S')

        return {'value':{'contract_mod_date': act_date}}
        #return True
        
project()


