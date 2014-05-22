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

from osv import fields, osv
from tools.translate import _

class idea_ext_isa(osv.osv):
    _inherit = 'idea.idea'
    
    def _create_url(self, cr, uid, ids, name, arg, context=None):

        results = self.pool.get('idea.idea').read(cr, uid, ids, ['name', 'user_id'])
        x={}
        x[ids[0]] = 'http://10.10.15.152/arcdoc/form01.php?cli=' + results[0]['name'] + '&user=' + results[0]['user_id'][1]
        return x

    _columns = {
        'customurl': fields.function(_create_url, string="Collegamento a documentale", type="char", method=True ),
    }

        
idea_ext_isa()
            
