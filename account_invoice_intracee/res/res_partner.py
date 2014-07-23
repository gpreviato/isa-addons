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
from openerp.tools.translate import _


class account_cee_res_partner(orm.Model):

    _inherit = "res.partner"

    _columns = {
        # Modo trasporto - alfa 1
        'way_of_freight': fields.many2one('account.cee.way.of.freight',
                                          'Way of freight'),
        # Modalita incasso servizi - alfa 1
        'payment_methods': fields.many2one('account.cee.payment.methods',
                                           'Payment Methods'),

        'country_provenance': fields.many2one('res.country',
                                              'Provenance Country'),

        'country_origin': fields.many2one('res.country',
                                          'Origin Country'),
        }

    def create(self, cr, user, vals, context=None):
        if context is None:
            context = {}

        if 'property_account_position' in vals and vals['property_account_position']:
            fiscal_obj = self.pool.get('account.fiscal.position')
            fiscal_data = fiscal_obj.browse(cr, user, vals['property_account_position'])
            if fiscal_data and fiscal_data.name == 'Regime Intra comunitario':
                if 'delivery' not in vals or not vals['delivery']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Condizioni di Consegna" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'way_of_freight' not in vals or not vals['way_of_freight']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Metodo di Trasporto" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'payment_methods' not in vals or not vals['payment_methods']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Metodi di Pagamento" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'country_provenance' not in vals or not vals['country_provenance']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Paese di Provenienza" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'country_origin' not in vals or not vals['country_origin']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Paese di Origine" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))

        res = super(account_cee_res_partner, self).create(cr, user, vals, context)

        return res

    def write(self, cr, user, ids, vals, context=None):
        if context is None:
            context = {}

        if ('property_account_position' in vals and vals['property_account_position']):
            fiscal_obj = self.pool.get('account.fiscal.position')
            fiscal_data = fiscal_obj.browse(cr, user, vals['property_account_position'])
            if fiscal_data and fiscal_data.name == 'Regime Intra comunitario':
                t_partner_data = self.browse(cr, user, ids, context=context)
                for t_partner in t_partner_data:

                    if 'delivery' not in vals and not t_partner.delivery:
                        raise orm.except_orm(_('Error!'),
                                             _('Campo "Condizioni di Consegna" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                    if 'way_of_freight' not in vals and not t_partner.way_of_freight:
                        raise orm.except_orm(_('Error!'),
                                             _('Campo "Metodo di Trasporto" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                    if 'payment_methods' not in vals and not t_partner.payment_methods:
                        raise orm.except_orm(_('Error!'),
                                             _('Campo "Metodi di Pagamento" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                    if 'country_provenance' not in vals and not t_partner.country_provenance:
                        raise orm.except_orm(_('Error!'),
                                             _('Campo "Paese di Provenienza" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                    if 'country_origin' not in vals and not t_partner.country_origin:
                        raise orm.except_orm(_('Error!'),
                                             _('Campo "Paese di Origine" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))

                if 'delivery' in vals and not vals['delivery']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Condizioni di Consegna" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'way_of_freight' in vals and not vals['way_of_freight']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Metodo di Trasporto" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'payment_methods' in vals and not vals['payment_methods']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Metodi di Pagamento" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'country_provenance' in vals and not vals['country_provenance']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Paese di Provenienza" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))
                if 'country_origin' in vals and not vals['country_origin']:
                    raise orm.except_orm(_('Error!'),
                                         _('Campo "Paese di Origine" obbligatorio se si imposta come posizione fiscale "Regime Intra comunitario"!'))

        res = super(account_cee_res_partner, self).write(cr,
                                                         user,
                                                         ids,
                                                         vals,
                                                         context)
        return res
