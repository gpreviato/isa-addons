# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
import account

class account_invoice_template_ext_isa(osv.osv):

    _inherit = 'account.invoice.template'

    def onchange_type(self, cr, uid, ids, type):
       res = {}

       journal_type='purchase'
       if type == 'out_invoice' or type == 'out_refund':
          journal_type='sale'

       journal_obj = self.pool.get('account.journal')
       journal_ids = journal_obj.search(cr, uid, [('type', '=', journal_type)])

       res['journal_id'] = ''
       if journal_ids:
            res['journal_id'] = journal_ids[0]
       dom = {'journal_id':  [('id', 'in', journal_ids)]}

       return {'value': res, 'domain': dom}

    _columns = {
        'journal_id': fields.many2one('account.journal', 'Account journal'),
        }

account_invoice_template_ext_isa()
