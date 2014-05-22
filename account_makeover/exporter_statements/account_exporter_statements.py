# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2013 ISA srl (<http://www.isa.it>)
#    All Rights Reserved
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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class account_exporter_statements(orm.Model):
    _name = "account.exporter.statements"
    _description = "Lettera d'intento"
    _columns = {
        'letter_number': fields.char('Letter Number',
                                     size=20),
        'partner_id': fields.many2one('res.partner',
                                'Partner'),
        'letter_date': fields.date('Letter Date'),
        'letter_type': fields.selection([('S', 'Single Operation'),
                                         ('P', 'Period'),
                                         ('T', 'Till Import')],
                                         'Letter Type'),
        'vat_code_id': fields.many2one('account.tax',
                                'VAT Exemption Code'),
        'period_start': fields.date('Period Start'),
        'period_end': fields.date('Period End'),
        'max_amount': fields.float('Max Amount'),
        'letter_status': fields.selection([('A', 'Active'),
                                         ('E', 'Expired'),
                                         ('R', 'Revocated')],
                                         'Letter Status'),
        'name': fields.char('Description',
                             size=80),
    }
    
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for doc in self.browse(cr, uid, ids):
            descr = ("%s") % (doc.letter_number)
            res.append((doc.id, descr))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                                                context=None, limit=100):
        if args is None:
            args = []
        if context is None:
            context = {}

        req_ids = self.search(cr, uid, args + 
                              [('letter_number', operator, name)],
                                limit=limit,
                                context=context)
        return self.name_get(cr, uid, req_ids, context=context)

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        
        exp_ids = self.search(cr, uid, [('partner_id', '=', partner_id),
                                        ('letter_status', '=', 'A')])
        if len(exp_ids) > 0:
                raise orm.except_orm(_('Error!'), _('This Partner already has an active exporter statements'))
               

        return {'value': {
                    'partner_id': partner_id,
                    }
        }
