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
import time
from tools.translate import _

CALL_CENTER_AVAILABLE_STATES = [
    ('draft', 'Draft'),
    ('open', 'Opened'),
    ('cancel', 'Cancelled'),
    ('done', 'Closed'),
    ('pending', 'Pending'),
    ('assign', 'Assigned'),
    ('refuse', 'Refused'),
    ('reject', 'Rejected'),
    ('process', 'In progress'),
]

CALL_CENTER_AVAILABLE_PRIORITIES = [
    ('0', 'Very urgent'),
    ('1', 'Urgent'),
    ('2', 'Normal'),
    ('3', 'Low'),
    ('4', 'Very Low'),
]

class call_center_ticket(crm.crm_case, osv.osv):
    #_name='crm.claim'
    _description = "Ticket"
    _inherit = 'crm.claim'
    
    def _get_default_partner_address(self, cr, uid, context=None):

        if context is None:
            context = {}
        return self.pool.get('res.users').browse(cr, uid, uid, context).address_id.id

    def _get_default_partner(self, cr, uid, context=None):
        if context is None:
            context = {}
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if not user.address_id:
            return False
        return user.address_id.partner_id.id
        
    def _get_default_email(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if not user.address_id:
            return False
        return user.address_id.email
    
    def _get_default_phone(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        if not user.address_id:
            return False
        return user.address_id.phone
    
    _columns = {
        'name_contact':fields.char('Name Contact', size=40, required=False), 
        'phone_contact':fields.char('Phone Contact', size=15, required=False), 
        'mail_contact':fields.char('Mail Contact', size=30, required=False),
        'ticket_id':fields.char('Ticket ID', size=10, required=False),
        'priority': fields.selection(CALL_CENTER_AVAILABLE_PRIORITIES, 'Priority'),
        'state': fields.selection(CALL_CENTER_AVAILABLE_STATES, 'State', size=16, readonly=True, 
                                  help='The state is set to \'Draft\', when a case is created.\
                                  \nIf the case is in progress the state is set to \'Open\'.\
                                  \nWhen the case is over, the state is set to \'Done\'.\
                                  \nIf the case needs to be reviewed then the state is set to \'Pending\'.'),    
    }
    
    _defaults = {
        'date': False,
        'partner_id': _get_default_partner, 
        'partner_address_id': _get_default_partner_address, 
        'email_from':_get_default_email, 
        'partner_phone':_get_default_phone
    }
    
    def case_open(self, cr, uid, ids, *args):
        """
            Open ticket
        """
        res = super(call_center_ticket, self).case_open(cr, uid, ids, *args)
        #import pdb; pdb.set_trace()
        
        date_open=time.strftime('%Y-%m-%d %H:%M:%S');
        
        ticket_id=self.pool.get('ir.sequence').get(cr, uid, 'call_center.ticket_id')
        self.write(cr,uid,ids,{'ticket_id':ticket_id,'date':date_open})
        
        ticket=self.browse(cr,uid,ids)[0]
        user=self.pool.get('res.users').browse(cr,uid,uid)
        #import pdb; pdb.set_trace()
        if not user.context_project_id.id:
            raise osv.except_osv(_('Invalid action !'), _('User type "Call Center / External Ticket Opener" must have a default project!'))
        
        issue={
            'name': ticket.name,
            'active': True,
            'section_id': ticket.categ_id.id,
            'partner_id': ticket.partner_id.id,
            'partner_address_id': ticket.partner_address_id.id,
            'partner_phone': ticket.partner_phone,
            'email_from': ticket.email_from,
            'company_id':ticket.company_id.id,
            'description': ticket.description,
            'state': 'open',
            'email_cc': ticket.email_cc,
            'date_open': ticket.date,
            #'date': ticket.date,
            'categ_id': ticket.categ_id.id,
            'priority': ticket.priority,
            #'partner_name': ticket.name_contact,
            'project_id':user.context_project_id.id,
            'user_id':ticket.user_id.id,
            'name_contact':ticket.name_contact,
            'phone_contact':ticket.phone_contact,
            'mail_contact':ticket.mail_contact,
            'ticket_id':ticket.ticket_id,
        }
        
        
       
       
        issue_obj=self.pool.get('project.issue')
        new_issue_id=issue_obj.create(cr,uid,issue)
        #import pdb; pdb.set_trace()
        issues=issue_obj.browse(cr,uid,[new_issue_id])
        issue_obj.history(cr, uid, issues, _('Open'))
        message=_("Issue '%s' opened from ticket: %s") % (ticket.name,ticket.ticket_id)
        issue_obj.history(cr, uid, issues, _('Note'),details=message)
               
        return res
        
    def unlink(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        tickets = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for t in tickets:
            if t['state'] in ('draft', 'cancel'):
                unlink_ids.append(t['id'])
            else:
                raise osv.except_osv(_('Invalid action !'), _('Cannot delete ticket(s) that are already opened!'))
        osv.osv.unlink(self, cr, uid, unlink_ids, context=context)
        return True
        
call_center_ticket()
    
