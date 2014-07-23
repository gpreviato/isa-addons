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

from openerp.osv import fields, orm


class account_incoterm_invoice_lines(orm.Model):

    _inherit = "account.invoice.line"

    _columns = {
            # Condizione di consegna - alfa 1
            'delivery': fields.many2one('stock.incoterms',
                                        'Condizione di consegna',
                                        help="International Commercial Terms are a series of predefined commercial terms used in international transactions."),
        }

    def _default_delivery(self, cr, uid, context=None):
        if ('partner_id' in context
                and 'fiscal_position' in context
                and self.check_intracee(cr, uid, context['fiscal_position'])):
            if (context['partner_id']):
                t_partner_id = context['partner_id']
                t_partner_obj = self.pool.get('res.partner')
                t_partner_search = t_partner_obj.search(cr, uid,
                                                [('id', '=', t_partner_id)])
                if (t_partner_search):
                    t_partner_data = t_partner_obj.browse(cr, uid,
                                                t_partner_search)[0]
                    if (t_partner_data
                            and t_partner_data.delivery
                            and t_partner_data.delivery.id):
                        return t_partner_data.delivery.id
        return None

    _defaults = {
        'delivery': _default_delivery,
    }
