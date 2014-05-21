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
from call_center import call_center_opener, call_center_manager
from tools.translate import _
import time

class call_center_technician(osv.osv):
    #_name = 'call_center.task'
    _description = 'Activities of the technician'
    _order = 'priority asc, create_date desc'
    _inherit = 'project.task'
    
    _columns = {
        'partner_address_id': fields.many2one('res.partner.address', 'Partner Contact', \
                                 domain="[('partner_id','=',partner_id)]"),
        'email_from': fields.char('Email', size=128, help="These people will receive email."),
        'partner_phone': fields.char('Phone', size=32),
        'result_description': fields.text('Reason for closure'),
        'name_contact':fields.char('Name Contact', size=40, required=False), 
        'phone_contact':fields.char('Phone Contact', size=15, required=False), 
        'mail_contact':fields.char('Mail Contact', size=30, required=False),
        'ticket_id':fields.char('Ticket ID', size=10, required=False), 
        'date_ticket': fields.datetime('Opened', readonly=True,select=True),
        'priority': fields.selection(call_center_opener.CALL_CENTER_AVAILABLE_PRIORITIES, 'Priority'),
        'state': fields.selection(call_center_opener.CALL_CENTER_AVAILABLE_STATES, 'State', size=16, readonly=True,
                                  help='The state is set to \'Draft\', when a case is created.\
                                  \nIf the case is in progress the state is set to \'Open\'.\
                                  \nWhen the case is over, the state is set to \'Done\'.\
                                  \nIf the case needs to be reviewed then the state is set to \'Pending\'.'),
          
    }
    
    def do_open(self, cr, uid, ids, *args):
        """
        Start task
        """
        res = super(call_center_technician, self).do_open(cr, uid, ids, *args)
        
        task = self.browse(cr,uid,ids)[0]

        # Update state to PROCESS to object issue(project.issue) if exists
        issue_obj = self.pool.get('project.issue')
        resource_issue = issue_obj.search(cr, uid, [('ticket_id','=',task.ticket_id)])
        
        if resource_issue and len(resource_issue):
            issue_obj.write(cr, uid, resource_issue, {'state': 'process',})
            message = _("The ticket '%s' has been accepted by '%s'.") % (task.ticket_id,task.user_id.name)
            issue_cases = issue_obj.browse(cr, uid, resource_issue)
            issue_obj.history(cr, uid, issue_cases, _('In progress'), history=False, )
            issue_obj.history(cr, uid, issue_cases, _('Note'), history=False, details=message,)
        
            # Update state to ASSIGN to object ticket(crm.claim) if exists
            ticket_obj = self.pool.get('crm.claim')
            resource_ticket = ticket_obj.search(cr, uid, [('ticket_id','=',task.ticket_id)])
            
            if resource_ticket and len(resource_ticket):
                ticket_obj.write(cr, uid, resource_ticket, {'state': 'process',})
                ticket_cases = ticket_obj.browse(cr, uid, resource_ticket)
                ticket_obj.history(cr, uid, ticket_cases, _('In progress'), history=False, )
            
        return True
        
    def case_reject(self, cr, uid, ids, context=None):
        """
        Reject task
        Set state to REJECT
        Update state to REJECT to object issue(project.issue) if exists
        Update state to REJECT to object ticket(crm.claim) if exists
        """
        #import pdb; pdb.set_trace()
        task=self.browse(cr,uid,ids)[0]
        
        self.write(cr,uid,ids,{'state': 'reject','result_description': context['reject_message']})
        
        # Update state to REJECT to object issue(project.issue) if exists
        issue_obj = self.pool.get('project.issue')
        resource_issue = issue_obj.search(cr, uid, [('ticket_id','=',task.ticket_id)])
        
        if resource_issue and len(resource_issue):
            issue_obj.write(cr, uid, resource_issue, {'state': 'reject', 'task_id': None, 'assigned_to': None, 'assigned_to_temp': None})
            message = _("The ticket '%s' has been rejected by '%s'.") % (task.ticket_id,task.user_id.name)
            new_message = ("%s\n%s %s") % (message, _("Reason for rejection:"), context['reject_message'])
            issue_cases = issue_obj.browse(cr, uid, resource_issue)
            issue_obj.history(cr, uid, issue_cases, _('Rejected'), history=False, )
            issue_obj.history(cr, uid, issue_cases, _('Note'), history=False, details=new_message,)

        return True
        
    def action_close(self, cr, uid, ids, context=None):
        """
        Close completed task
        This action open wizard to send email to partner or project manager after close task.
        """
        
        task = self.browse(cr,uid,ids)[0]
        
        if not task.result_description:
            raise osv.except_osv(_('The reason for the closure is required!'),_("To complete the call you have to fill in the field 'Reason for closure'."))
            return False
            
        res = super(call_center_technician, self).action_close(cr, uid, ids, context)
        
        # Update state to DONE to object issue(project.issue) if exists
        issue_obj = self.pool.get('project.issue')
        resource_issue = issue_obj.search(cr, uid, [('ticket_id','=',task.ticket_id)])
        
        if resource_issue and len(resource_issue):
            issue_obj.write(cr, uid, resource_issue, {'state': 'done',})
            message = _("The ticket '%s' has been completed and closed by '%s'.") % (task.ticket_id,task.user_id.name)
            new_message = ("%s\n%s %s") % (message, _("Result:"), task.result_description)
            issue_cases = issue_obj.browse(cr, uid, resource_issue)
            issue_obj.history(cr, uid, issue_cases, _('Completed'), history=False, )
            issue_obj.history(cr, uid, issue_cases, _('Note'), history=False, details=new_message,)
        
            # Update state to DONE to object ticket(crm.claim) if exists
            ticket_obj = self.pool.get('crm.claim')
            resource_ticket = ticket_obj.search(cr, uid, [('ticket_id','=',task.ticket_id)])
            
            if resource_ticket and len(resource_ticket):
                ticket_obj.write(cr, uid, resource_ticket, {'state': 'done',})
                message = _("The ticket '%s' has been completed.") % (task.ticket_id)
                new_message = ("%s\n%s %s") % (message, _("Result:"), task.result_description)
                ticket_cases = ticket_obj.browse(cr, uid, resource_ticket)
                ticket_obj.history(cr, uid, ticket_cases, _('Completed'), history=False, )
                ticket_obj.history(cr, uid, ticket_cases, _('Note'), history=False, details=new_message,)
        
        return res
            
call_center_technician()

