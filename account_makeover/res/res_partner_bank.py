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

from openerp.osv import orm


class res_partner_bank_ext_isa(orm.Model):
    _inherit = 'res.partner.bank'
    
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for partner_bank in self.browse(cr, uid, ids):
            descr = ("%s [ %s ]") % (partner_bank.acc_number,
                                     partner_bank.bank.name)
            res.append((partner_bank.id, descr))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                                                context=None, limit=100):
        if args is None:
            args = []
        if context is None:
            context = {}

        req_ids = self.search(cr, uid, args + 
                              ['|',
                               ('acc_number', operator, name),
                               ('bank.name', operator, name)],
                                limit=limit,
                                context=context)
        return self.name_get(cr, uid, req_ids, context=context)
