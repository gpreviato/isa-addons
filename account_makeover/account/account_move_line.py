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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class account_move_line_makeover(orm.Model):
    _inherit = 'account.move.line'

    def get_invoice(self, cr, uid, ids, context=None):
        invoice_pool = self.pool.get('account.invoice')
        res = {}
        for line in self.browse(cr, uid, ids):
            t_line_id = line.move_id.id
            inv_ids = invoice_pool.search(cr, uid,
                                          [('move_id', '=', t_line_id)])
            if len(inv_ids) > 1:
                raise orm.except_orm(_('Error'), _('Incongruent data: move %s has more than one invoice') % line.move_id.name)
            if inv_ids:
                res[line.id] = inv_ids[0]
            else:
                res[line.id] = False
        return res

    def _sign_amount(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context):
            if(line.credit > 0):
                res[line.id] = line.credit
            else: 
                res[line.id] = -line.debit
        return res

    _columns = {
        'payment_type': fields.selection([('C', 'Cash'),
                                          ('B', 'Bank Transfer'),
                                          ('D', 'Bank Draft')],
                                         'Payment Type',),
        'is_selected': fields.selection([('draft', 'Draft'),
                                         ('accepted', 'Accepted'),
                                         ('valid', 'Valid')],
                                        'Selection Type'),
        'document_number': fields.related('move_id', 'document_number',
                                          type='char',
                                          relation='account.move',
                                          string='Document Number'),
        'currency_date': fields.date('Currency Date'),
        'fnct_amount': fields.function(_sign_amount,
                                       string='Amount',
                                       type='float'),
        'is_wht': fields.boolean('Withholding tax'),
        'wht_state': fields.selection([('open', 'Open'),
                                       ('confirmed', 'Confirmed'),
                                       ('selected', 'Selected'),
                                       ('paid', 'Paid')], 'Wht State'),
        }

    _defaults = {
        'state': 'draft',
        'is_wht': False,
        'wht_state': None
        }
