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


class account_payment_term_line_makeover(orm.Model):
    _inherit = "account.payment.term.line"

    _columns = {
                'payment_type': fields.selection([
                                                  ('C', 'Cash'),
                                                  ('B', 'Bank Transfer'),
                                                  ('D', 'Bank Draft')],
                                                 'Payment Type',
                                                 required=True),
            }

    _defaults = {
                 'payment_type': 'C',
                 }
