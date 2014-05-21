# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
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

from datetime import datetime
import time

from osv import fields, osv
from tools.translate import _

#----------------------------------------------------------
# Identification Depots. 
#----------------------------------------------------------
class depot(osv.osv):
    _name = "depot"
    _description = "Depots"

    _columns = {
        'name': fields.char('Code', size=10, required=True,),
        'location': fields.char('Location', size=255, required=True,),
        'description': fields.char('Description', size=70,),
        'opened': fields.boolean('Opened'),
        'move_ids':fields.one2many('depot.move','depot_id','Depot moves', readonly=True, domain=[('state', '=', 'waiting'),] )
    }
    
    _defaults = {
        'opened': True,
    }
    
    _order = 'name asc'
    
depot()


#----------------------------------------------------------
# Depot movements. 
#----------------------------------------------------------
class depot_move(osv.osv):
    _name = "depot.move"
    _description = "Depot movements"

    _columns = {
        'name': fields.char('License plate', size=10, required=True,),
        'qty': fields.integer('Quantity', required=False,),
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer', '=', True),], select=True, ondelete="cascade",),
        'depot_id': fields.many2one('depot', 'Depot Code', required=True, domain=[('opened', '=', True),], select=True, ondelete='cascade',),
        'date_storage': fields.datetime('Storage date', select=True),
        'date_pickup': fields.datetime('Pick-up date', select=True),
        'date_pickup_scheduled': fields.datetime('Pick-up date scheduled', select=True),
        'state': fields.selection([('draft', 'Draft'), ('waiting', 'In storage'), ('done', 'Returned'), ], 'State', readonly=True, select=True),
        'desc1': fields.char('Description 1', size=20, required=False,),
        'dot1': fields.char('DOT 1', size=20, required=False,),
        'desc2': fields.char('Description 2', size=20, required=False,),
        'dot2': fields.char('DOT 2', size=20, required=False,),
        'desc3': fields.char('Description 3', size=20, required=False,),
        'dot3': fields.char('DOT 3', size=20, required=False,),
        'desc4': fields.char('Description 4', size=20, required=False,),
        'dot4': fields.char('DOT 4', size=20, required=False,),
    }

    _defaults = {
        'state': 'draft',
        #'qty': 0,
        'date_storage': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    _order = 'date_storage desc'

    def action_deposit_tires(self, cr, uid, ids, context=None):
        """ 
        Create deposit movement and change status to "In storage"
        """
        data = {}
        data['state'] = 'waiting'
        
        move_obj = self.pool.get('depot.move')
        movement=self.browse(cr,uid,ids)[0]
        """
        if not movement.qty:
            raise osv.except_osv(_('Quantity zero !'), _('The field "Quantity" must have a value greater than zero'))
            return False
        """
        
        res = self.write(cr,uid,ids,data)
        if res == True:
            self.log(cr, uid, movement.id, _('Items "In storage" for movement n.%s') % movement.id)
        else:
            self.log(cr, uid, movement.id, _('Error status change in movement n.%s') % movement.id)
        return res            

    def action_picks_up_tires(self, cr, uid, ids, context=None):
        """ 
        Create deposit movement and change status to "Returned"
        """
        data = {}
        data['state'] = 'done'
        
        move_obj = self.pool.get('depot.move')
        movement=self.browse(cr,uid,ids)[0]
        if not movement.date_pickup:
            data['date_pickup'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
        res = self.write(cr,uid,ids,data)
        if res == True:
            self.log(cr, uid, movement.id, _('Items "Returned" for movement n.%s') % movement.id)
        else:
            self.log(cr, uid, movement.id, _('Error status change in movement n.%s') % movement.id)
        return res            

depot_move()

