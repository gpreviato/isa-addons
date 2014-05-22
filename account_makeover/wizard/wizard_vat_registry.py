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

from openerp.osv import fields, orm
from openerp.tools.translate import _


class wizard_vat_registry(orm.TransientModel):
    _name = 'wizard.vat.registry'
    _description = 'Wizard Vat Registry'

    def get_print(self, cr, uid, ids, context):
        data = self.read(cr, uid, ids)[0]
        t_report_name = 'vat_registry'
        if data['print_landscape']:
            t_report_name = 'vat_registry_landscape'
        datas = {
             'ids': [],
             'model': 'account.invoice',
             'context': context.get('active_ids', []),
             'form': data
                 }

        return {
           'type': 'ir.actions.report.xml',
           'datas': datas,
           'report_name': t_report_name,
        }

    def _get_default_period(self, cr, uid, context=None):

        ctx = dict(context or {},
                   account_period_prefer_normal=True)
        period_obj = self.pool.get('account.period')
        period_ids = period_obj.find(cr, uid,
                                     context=ctx)
        return period_ids[0] 

    _columns = {
        'vat_register': fields.many2one('vat.registries.isa',
                                        'VAT Register'),
        'period_id': fields.many2one('account.period',
                                     'Period',
                                     required=True),
        'draft_or_ok': fields.selection([
            ('draft', 'Draft'),
            ('ultimate', 'Ultimate'),
        ], 'Print Type', size=32),
        'print_landscape': fields.boolean('Orientamento orizzontale'),
    }

    _defaults = {
        'period_id': _get_default_period,
        'print_landscape': False,
    }
