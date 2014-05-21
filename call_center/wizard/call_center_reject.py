# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

DEFAULT_REJECT_MESSAGE = _("The call is not relevant.")

class rejection_wizard(osv.osv_memory): 
    _name = 'call_center.reject'
    _description = "Reason for rejection"
    
    _columns = { 
        'message': fields.text('Message', required=True),
    }
    
    _defaults = {
        'message':  DEFAULT_REJECT_MESSAGE,
    }
    
    def do_reject(self, cr, uid, ids, context=None, *args):
        model_obj=self.pool.get(context['active_model'])

        model=model_obj.browse(cr, uid, context['active_ids'])[0]
        
        reject=self.browse(cr,uid,ids)[0]
        
        text_reject=_("REASON FOR REJECTION")
        
        new_description=u'%s\n---------------------- %s -------------------\n%s' % (model.description,text_reject,reject.message.decode('utf8'))
        
        if context['case_type'] == 'refuse':
            model_obj.write(cr,uid,context['active_ids'],{'description':new_description})
            model_obj.case_refuse(cr, uid, context['active_ids'], context)
        elif context['case_type'] == 'reject': 
            context['reject_message'] = reject.message.decode('utf8')
            model_obj.case_reject(cr, uid, context['active_ids'], context)
        
        return {'type': 'ir.actions.act_window_close'}
 
rejection_wizard()
