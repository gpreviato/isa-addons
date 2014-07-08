# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
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


class wizard_vat_registry(orm.TransientModel):

    _name = "wizard.vat.registry"

    def _get_period(self, cr, uid, context=None):
        ctx = dict(context or {}, account_period_prefer_normal=True)
        period_ids = self.pool.get('account.period').find(cr, uid, context=ctx)
        return period_ids

    _columns = {
        'period_ids': fields.many2many('account.period',
                                       'registro_iva_periods_rel',
                                       'period_id',
                                       'registro_id',
                                       'Periodi',
                                       help='Select periods you want retrieve documents from',
                                       required=True),
        'tax_sign': fields.float('Segno Importi Tasse',
            help="Use -1 you have negative tax amounts and you want to print them as positive"),
        'message': fields.char('Messaggio', size=64,
                                       readonly=True),
        'fiscal_page_base': fields.integer('Ultima Pagina Stampata',
                                       required=True),
        'iva_registry_id': fields.many2one('vat.registries.isa',
                                       'Registro',
                                       required=True),
        'padding': fields.integer('Padding', 
                                  require=True)
        }

    _defaults = {
        'period_ids': _get_period,
        'tax_sign': 1.0,
        'fiscal_page_base': 0,
        'padding':0,
        }

    def print_registro(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wizard = self.browse(cr, uid, ids)[0]
        move_obj = self.pool.get('account.move')
        obj_model_data = self.pool.get('ir.model.data')

        journal_obj = self.pool.get('account.journal')
        t_iva_registry_id = wizard.iva_registry_id
        t_journal_ids = journal_obj.search(cr, uid,
                                    [('iva_registry_id', '=', t_iva_registry_id.id)])

        t_layout_type = wizard.iva_registry_id.layout_type
        if not t_layout_type:
            raise orm.except_orm(_('Error'), _('Nessun Layout Stampa definito per questo Registro.'))

        if isinstance(t_journal_ids, (int, long)):
            t_journal_ids = [t_journal_ids]
        move_ids = move_obj.search(cr, uid, [
            ('journal_id', 'in', [j for j in t_journal_ids]),
            ('period_id', 'in', [p.id for p in wizard.period_ids]),
            ('state', '=', 'posted'),
            ], order='date, name')
        if not move_ids:
            self.write(cr, uid,  ids, {'message': _('No documents found in the current selection')})
            model_data_ids = obj_model_data.search(cr, uid, [('model','=','ir.ui.view'), ('name','=','wizard_vat_registry')])
            resource_id = obj_model_data.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
            return {
                'name': _('No documents'),
                'res_id': ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.vat.registry',
                'views': [(resource_id,'form')],
                'context': context,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        datas = {'ids': move_ids}
        datas['model'] = 'account.move'
        datas['fiscal_page_base'] = wizard.fiscal_page_base
        datas['period_ids'] = [p.id for p in wizard.period_ids]
        datas['layout'] = t_layout_type
        datas['tax_sign'] = wizard['tax_sign']
        datas['iva_registry_id'] = wizard['iva_registry_id'].id
        datas['padding'] = wizard['padding']
        res= {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }
        if t_layout_type == 'customer':
            res['report_name'] = 'vat_registry_sale_webkit'
        elif t_layout_type == 'supplier':
            res['report_name'] = 'vat_registry_purchase_webkit'
        elif t_layout_type == 'corrispettivi':
            res['report_name'] = 'vat_registry_corrispettivi_webkit'
        return res

    def onchange_iva_registry_id(self, cr, uid, ids,
                                          iva_registry_id,
                                          context=None):
        if context is None:
            context = {}
        res={}
        warning = {}
        if iva_registry_id:
            registry_obj = self.pool.get('vat.registries.isa')
            registry_data = registry_obj.browse(cr, uid,
                                        iva_registry_id,
                                        context)
            if registry_data:
                if registry_data.sequence_iva_registry_id.prefix:
                    warning = {
                               'title': _('Warning!'),
                               'message': _('This sequence is not allowed because it contains a prefix')
                               }
                    return {'value': {},
                            'warning': warning,
                             }
                if registry_data.sequence_iva_registry_id.suffix:
                    warning = {
                               'title': _('Warning!'),
                               'message': _('This sequence is not allowed because it contains a suffix')
                               }
                    return {'value': {},
                            'warning': warning,
                             }

            if registry_data and registry_data.layout_type:
                if registry_data.layout_type == 'supplier':
                    res['value'] = {'tax_sign': -1}
                else:
                    res['value'] = {'tax_sign': 1}
                return res

        return {'value': {},
                'warning': warning,
                 }