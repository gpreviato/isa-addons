# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 ISA s.r.l. (<http://www.isa.it>).
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

from openerp.osv import fields, osv
from tools.translate import _

class account_invoice_bank_partner_ext_isa(osv.osv):
    #_name = 'account.invoice'
    _inherit = 'account.invoice'

    def onchange_partner_id(self, cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        """
                Extends the onchange.
        """
        result = super(account_invoice_bank_partner_ext_isa, self).onchange_partner_id(cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False)

        if partner_id:
            result['value']['bank_account'] = ''

        return result

    _columns = {
        'bank_account': fields.many2one('res.partner.bank', 'Bank Account of Client',  readonly=True, states={'draft':[('readonly',False)]}),
        'partner_bank_id': fields.many2one('res.partner.bank', 'Company Bank',  readonly=True, states={'draft':[('readonly',False)]}),
    }

account_invoice_bank_partner_ext_isa()
