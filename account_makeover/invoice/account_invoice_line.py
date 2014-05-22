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


class account_invoice_line_makeover(orm.Model):
    _inherit = "account.invoice.line"

    _columns = {
        'account_user_report_type': fields.related(
                                       'account_id',
                                       'user_type',
                                       'report_type',
                                       type='char',
                                       relation='account.account.type',
                                       string='Account Type',
                                       readonly=1),
    }

    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0,
                          name='', type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False,
                          currency_id=False, context=None, company_id=None):
        if context is None:
            context = {}
        exporter_id = context.get('exporter_id', None)
        doc_date = context.get('date_invoice', None)
        if not company_id:
            return {'value': {}}
        res = super(account_invoice_line_makeover, self).product_id_change(cr, uid, ids, product, uom_id, qty, name, type, partner_id, fposition_id, price_unit, currency_id, context, company_id)
        if(exporter_id):
            exp_obj = self.pool.get('account.exporter.statements')
            t_exp = exp_obj.browse(cr, uid, exporter_id)
            if(t_exp.letter_status == 'A'):
                if (t_exp.letter_type != 'P'):
                    res['value'].update({'invoice_line_tax_id': [t_exp.vat_code_id.id]})
                elif(doc_date > t_exp.period_start and doc_date < t_exp.period_end):
                    res['value'].update({'invoice_line_tax_id': [t_exp.vat_code_id.id]})
        return res
