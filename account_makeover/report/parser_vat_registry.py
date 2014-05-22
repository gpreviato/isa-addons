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

import locale
from openerp.report import report_sxw
from openerp import pooler
import os

class parser_vat_registry(report_sxw.rml_parse):
    _name = 'parser_vat_registry'
    
    def __init__(self, cr, uid, name, context):
        self.cr = cr
        self.uid = uid
        self.filters = []
        self.context = context
        self.date_start = None
        self.date_stop = None
        self.date_year = None
        self.registry_name = None

        super(parser_vat_registry, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_vat_registry_lines': self._get_vat_registry_lines,
            'get_total_selected': self._get_total_selected,
            'get_total_start_year': self._get_total_start_year,
            'set_dates': self._set_dates,
            'get_registry_name': self._get_registry_name,
            'get_date_start': self._get_date_start,
            'get_date_stop': self._get_date_stop,
            'get_date_year': self._get_date_year,
            'locale': locale,
            'get_ref_autoinvoice': self._get_ref_autoinvoice,
        })

    def _get_registry_name(self):
        return self.registry_name

    def _get_date_start(self):
        return self.date_start

    def _get_date_stop(self):
        return self.date_stop

    def _get_date_year(self):
        return self.date_year

    def _set_dates(self, form_values, selected_items):
        t_period_obj = pooler.get_pool(self.cr.dbname).get('account.period')
        t_period_id = form_values['period_id'][0]
        t_period_data = t_period_obj.browse(self.cr, self.uid, t_period_id)
        self.date_start = t_period_data.date_start
        self.date_stop = t_period_data.date_stop
        end_date = self.date_stop.split("-")
        self.date_year = end_date[0]
        
        t_registry_obj = pooler.get_pool(self.cr.dbname).get('vat.registries.isa')
        t_vat_registry = form_values['vat_register'][0]
        t_registry_data = t_registry_obj.browse(self.cr, self.uid, t_vat_registry)
        self.registry_name = t_registry_data.name

    def _get_vat_registry_lines(self, form_values, selected_items):

        t_vat_register = form_values['vat_register'][0]

        query = """
                SELECT
                     "account_invoice"."number" as num_documento,
                     "account_invoice"."protocol_number" as protocol_number,
                     "account_invoice"."supplier_invoice_number" as supplier_invoice_number,
                     "account_invoice"."date_invoice",
                     "account_invoice"."ref_autoinvoice",
                     "account_invoice_tax"."base_amount" as imponibile,
                     "account_invoice_tax"."tax_amount" as imposta,
                     "account_invoice_tax"."base_amount" + "account_invoice_tax"."tax_amount" as tot_riga,
                     "account_tax_code"."code" as cod_iva,
                     "account_tax_code"."name",
                     "account_journal"."name" as sezionale,
                     "account_journal"."code" as cod_sezionale,
                     "vat_registries_isa"."name" as nome_registro,
                     "res_partner"."name" as cliente,
                     AZIENDA.vat AS p_iva_azienda,
                     AZIENDA.street AS via_azienda,
                     AZIENDA.city AS citta_azienda,
                     AZIENDA.zip AS zip_azienda,
                     AZIENDA.email AS email_azienda,
                     AZIENDA.phone AS phone_azienda,
                     AZIENDA.name AS nome_azienda,
                     "res_company".logo_web,
                     CAST(coalesce(account_invoice.protocol_number, '0') AS integer) as order_number
                FROM
                     "account_invoice"
                     INNER JOIN "account_invoice_tax" ON "account_invoice"."id" = "account_invoice_tax"."invoice_id"
                     INNER JOIN "account_tax_code" ON "account_invoice_tax"."tax_code_id" = "account_tax_code"."id"
                     INNER JOIN "account_journal" ON "account_invoice"."journal_id" = "account_journal"."id"
                     INNER JOIN "res_partner" ON "account_invoice"."partner_id" = "res_partner"."id"
                     LEFT JOIN  "vat_registries_isa" ON "account_journal"."iva_registry_id" = "vat_registries_isa"."id"
                     INNER JOIN "res_company" ON "account_invoice"."company_id" = "res_company"."id"
                                              AND "res_company"."id" = "res_partner"."company_id"
                     LEFT JOIN "res_partner" AS AZIENDA ON "res_company"."partner_id" = AZIENDA."id"  
                WHERE 
                     ("account_invoice"."registration_date" >= '""" + self.date_start + """')
                     AND ("account_invoice"."registration_date" <= '""" + self.date_stop + """')
                     AND ("account_invoice"."state" not like 'draft')
                     AND "vat_registries_isa"."id" =  """ + str(t_vat_register) + """
                order by order_number asc
                """

        self.cr.execute(query)
        res = self.cr.dictfetchall()
        
        t_last_date_invoice = self.date_start
        t_list = []
        for item in res:
            t_actual_date_invoice = item['date_invoice']
            t_protocol_date = item['date_invoice']
            if t_actual_date_invoice < t_last_date_invoice:
                t_protocol_date = t_last_date_invoice
            else:
                t_last_date_invoice = item['date_invoice']

            item.update({'protocol_date': t_protocol_date})

            t_list.append(item)

        return t_list

    def _get_ref_autoinvoice(self, invoice_id):

        t_invoice_obj = pooler.get_pool(self.cr.dbname).get('account.invoice')
        if invoice_id:
            t_invoice_data = t_invoice_obj.browse(self.cr, self.uid, [invoice_id])
            for t_invoice in t_invoice_data:
                t_ref_autoinvoice = t_invoice.number
                if t_invoice.id == invoice_id:
                    return t_ref_autoinvoice
        return None

    def _get_total_selected(self, form_values, selected_items):

        t_vat_register = form_values['vat_register'][0]

        query = """
                SELECT
                     sum("account_invoice_tax"."base_amount") as imponibile,
                     sum("account_invoice_tax"."tax_amount") as imposta,
                     sum("account_invoice_tax"."base_amount") + sum("account_invoice_tax"."tax_amount") as tot_riga,
                     "account_tax_code"."code" as cod_iva,
                     "account_tax_code"."name"
                FROM
                     "account_invoice" 
                     INNER JOIN "account_invoice_tax" ON "account_invoice"."id" = "account_invoice_tax"."invoice_id"
                     INNER JOIN "account_tax_code" ON "account_invoice_tax"."tax_code_id" = "account_tax_code"."id"
                     INNER JOIN "account_journal" ON "account_invoice"."journal_id" = "account_journal"."id"
                     LEFT JOIN  "vat_registries_isa" ON "account_journal"."iva_registry_id" = "vat_registries_isa"."id"
                WHERE
                     ("account_invoice"."registration_date" >= '""" + self.date_start + """')
                     AND ("account_invoice"."registration_date" <= '""" + self.date_stop + """')
                     AND "vat_registries_isa"."id" =  """ + str(t_vat_register) + """
                GROUP BY
                     "account_tax_code"."code", "account_tax_code"."name"
                """

        self.cr.execute(query)
        res = self.cr.dictfetchall()

        return res

    def _get_total_start_year(self, form_values, selected_items):

        t_vat_register = form_values['vat_register'][0]

        query = """
                SELECT
                     sum("account_invoice_tax"."base_amount") as imponibile,
                     sum("account_invoice_tax"."tax_amount") as imposta,
                     sum("account_invoice_tax"."base_amount") + sum("account_invoice_tax"."tax_amount") as tot_riga,
                     "account_tax_code"."code" as cod_iva,
                     "account_tax_code"."name"
                FROM
                     "account_invoice" 
                     INNER JOIN "account_invoice_tax" ON "account_invoice"."id" = "account_invoice_tax"."invoice_id"
                     INNER JOIN "account_tax_code" ON "account_invoice_tax"."tax_code_id" = "account_tax_code"."id"
                     INNER JOIN "account_journal" ON "account_invoice"."journal_id" = "account_journal"."id"
                     LEFT JOIN  "vat_registries_isa" ON "account_journal"."iva_registry_id" = "vat_registries_isa"."id"
                WHERE
                     ("account_invoice"."registration_date" >= '""" + self.date_year + """-01-01')
                     AND ("account_invoice"."registration_date" <= '""" + self.date_stop + """')
                     AND "vat_registries_isa"."id" =  """ + str(t_vat_register) + """
                GROUP BY
                     "account_tax_code"."code", "account_tax_code"."name"
                """

        self.cr.execute(query)
        res = self.cr.dictfetchall()

        return res

report_sxw.report_sxw('report.vat_registry',
                       'account.invoice',
                       os.path.dirname(os.path.realpath(__file__)) + '/vat_registry.mako',
                       parser=parser_vat_registry)

report_sxw.report_sxw('report.vat_registry_landscape',
                       'account.invoice',
                       os.path.dirname(os.path.realpath(__file__)) + '/vat_registry.mako',
                       parser=parser_vat_registry)
