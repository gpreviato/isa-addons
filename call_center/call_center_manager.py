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
from crm import crm
from call_center import call_center_opener
from tools.translate import _
import time

class call_center_manager(crm.crm_case, osv.osv):
    #_name = 'call_center.manager'
    _description = 'Call Routing'
    _order = 'priority asc, date_open desc'
    _inherit = 'project.issue'
    
    _columns = {
        'name_contact':fields.char('Name Contact', size=40, required=False), 
        'phone_contact':fields.char('Phone Contact', size=15, required=False), 
        'mail_contact':fields.char('Mail Contact', size=30, required=False),
        'ticket_id':fields.char('Ticket ID', size=10, required=False), 
        'assigned_to_temp': fields.many2one('res.users', 'Assigned to'),
        'priority': fields.selection(call_center_opener.CALL_CENTER_AVAILABLE_PRIORITIES, 'Priority'),
        'state': fields.selection(call_center_opener.CALL_CENTER_AVAILABLE_STATES, 'State', size=16, readonly=True,
                                  help='The state is set to \'Draft\', when a case is created.\
                                  \nIf the case is in progress the state is set to \'Open\'.\
                                  \nWhen the case is over, the state is set to \'Done\'.\
                                  \nIf the case needs to be reviewed then the state is set to \'Pending\'.'),
          
    }
    
    def case_open(self, cr, uid, ids, *args):
        """
        Open internal ticket
        """
        res = super(call_center_manager, self).case_open(cr, uid, ids, *args)
        
        date_open=time.strftime('%Y-%m-%d %H:%M:%S');
        
        ticket_id=self.pool.get('ir.sequence').get(cr, uid, 'call_center.ticket_id')
        self.write(cr,uid,ids,{'ticket_id':ticket_id,'date':date_open,})
        
        return res
    
    def case_assign(self, cr, uid, ids, context=None):
        """
        Convret ticket to task
        Set state to ASSIGN
        Update ticket fields (priority,project_id)
        Update state to ASSIGN to object ticket(crm.claim)
        """
        #import pdb; pdb.set_trace()
        
        check_operator = self._check_operator(cr, uid, ids)
        
        if check_operator:
            issue=self.browse(cr,uid,ids)[0]
            
            # Convet ticket to task if not exits
            task_obj = self.pool.get('project.task')

            if not issue.task_id.id:
                res = super(call_center_manager, self).convert_issue_task(cr, uid, ids, context)
                task_values={
                    'state': 'assign',
                    'ticket_id': issue.ticket_id,
                    'date_ticket':issue.date_open,
                    'name_contact':issue.name_contact,
                    'phone_contact':issue.phone_contact,
                    'mail_contact':issue.mail_contact,
                    'partner_address_id': issue.partner_address_id.id,
                    'partner_phone': issue.partner_phone,
                    'email_from': issue.email_from,
                }
                task_obj.write(cr,uid,res['res_id'],task_values)
                    
            issue_values={
                'state': 'assign',
                'priority': issue.priority,
                'project_id': issue.project_id.id,
                'assigned_to': issue.assigned_to_temp.id,
            }
            
            self.write(cr,uid,ids,issue_values)
            
            cases = self.browse(cr, uid, ids)
            message = _("The ticket '%s' has been assigned to '%s'.") % (issue.ticket_id,issue.assigned_to_temp.name)
            self.history(cr, uid, cases, _('Assigned'), history=False, details=message,)
            self.history(cr, uid, cases, _('Note'), history=False, details=message,)
            
            # Update state to ASSIGN to object ticket(crm.claim) if exists
            ticket_obj = self.pool.get('crm.claim')
            resource_ticket = ticket_obj.search(cr, uid, [('ticket_id','=',issue.ticket_id)])
            
            if resource_ticket and len(resource_ticket):
                ticket_obj.write(cr, uid, resource_ticket, {'state': 'assign',})
                ticket_cases = ticket_obj.browse(cr, uid, resource_ticket)
                ticket_obj.history(cr, uid, ticket_cases, _('Assigned'), history=False, )
        
        return check_operator
                 
    def case_open_and_assigns(self, cr, uid, ids, context=None, *args):
        result = self._check_operator(cr, uid, ids)
        if result:
            self.case_open(cr, uid, ids, *args)
            self.case_assign(cr, uid, ids, context)
        
        return result
    
    def case_refuse(self, cr, uid, ids, context=None):
        """
        Refuse ticket
        Set state to REFUSE
        Update state to REFUSE to object ticket(crm.claim)
        """
        #import pdb; pdb.set_trace()
        issue=self.browse(cr,uid,ids)[0]
        
        self.write(cr,uid,ids,{'state': 'refuse', 'assigned_to_temp': None})
        
        cases = self.browse(cr, uid, ids)
        message = _("The ticket '%s' has been refused by %s.") % (issue.ticket_id, issue.user_id.name)
        self.history(cr, uid, cases, _('Refused'), history=False, details=message,)
        self.history(cr, uid, cases, _('Note'), history=False, details=message,)
        
        # Update state to REFUSE to object ticket(crm.claim) if exists
        ticket_obj = self.pool.get('crm.claim')
        resource_ticket = ticket_obj.search(cr, uid, [('ticket_id','=',issue.ticket_id)])
        
        if resource_ticket and len(resource_ticket):
            ticket_obj.write(cr, uid, resource_ticket, {'state': 'refuse','description':issue.description})
            ticket_cases = ticket_obj.browse(cr, uid, resource_ticket)
            ticket_obj.history(cr, uid, ticket_cases, _('Refused'), history=False,)
        
        return True
        
    def _check_operator(self,cr,uid,ids):
        issue=self.browse(cr,uid,ids)[0]
        
        if not issue.assigned_to_temp.id:
            raise osv.except_osv(_('Unknown operator !'), _('To continue, you must select an operator in the field "Assigned to".'))
            return False

        return True
            
call_center_manager()

