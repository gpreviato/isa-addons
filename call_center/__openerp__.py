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

{
    'name': 'Call Center module',
    'version': '0.1',
    'category': 'crm',
    'description': """
Call Center module that covers:
    Ticket Open
    Call Routing
    Task Manager

This module extends:
    CRM Claim
    Project Issue
    Project Task
       """,
    'author': 'ISA srl',
    'depends': ['crm_claim','project_issue'],
    'update_xml': [
        'security/call_center_security.xml',
        'security/ir.model.access.csv',
        'wizard/call_center_reject_view.xml',
        'call_center_view.xml',
        'call_center_manager_view.xml',
        'call_center_technician_view.xml',
        'ticket_sequence.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
