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

import time

from osv import osv, fields

class depot_move_tree_filter(osv.osv_memory):
    _name = 'depot.move.tree.filter'
    _description = 'Search filter for printing the list of movements of deposit'
    _columns = {
        'depot_id': fields.many2one('depot', 'Depot Code', domain=[('opened', '=', True),],),
        'date_storage_from': fields.date('From the date'),
        'date_storage_to': fields.date('at the date'),
        'date_pickup_from': fields.date('From the date'),
        'date_pickup_to': fields.date('at the date'),
        'date_pickup_scheduled_from': fields.date('From the date'),
        'date_pickup_scheduled_to': fields.date('at the date'),
    }
   
    def print_report(self, cr, uid, ids, context={}):
        datas = {
             'ids': [],
             'model': 'depot.move',
             'form': self.read(cr, uid, ids)[0]
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'depot_move_tree',
            'datas': datas,
        }

depot_move_tree_filter()
