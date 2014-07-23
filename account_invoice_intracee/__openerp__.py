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
{
    'name': "Account Invoice Intracee",
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Fatture di Acquisto Intracomunitarie
====================================

Configurazione
--------------
Per consentire la vlidazione di una fattura Intracee è necessario che l'Azienda
abbia i campi "Giornale Autofattura per Intracee" e "Girocredito per Intracee"
correttamente impostati; nel menu Configurazione andare su Aziende e per ogni
azienda impostare i campi obbligatori nella tab Configurazione.



Note
----
Il modulo "purchase" è impostato come dipendenza per ovviare
al seguente problema.
Il modulo "account_invoice_intracee" permette la visualizzazione di
righe di una fattura in una popup. Se il modulo account di openerp base
è installato senza che lo sia anche il modulo "purchase",
allora nella popup di una riga di una fattura fornitore, cliccando su
prodotto, si ottiene un errore.
L'installazione di purchase è un modo per evitare tale comportamento, in
attesa che il problema sia risolto.

    """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'depends' : ['account',
                 'account_makeover',
                 'account_voucher',
                 'purchase',
                 'base',
                 'stock_makeover',
                 'l10n_it_base'],
    'data' : [
              'security/ir.model.access.csv',
              'voucher/account_voucher_payment_intracee.xml',
              'security/intracee_group.xml',
              'cee/account_cee_tables_view.xml',
              'product/product_product_view.xml',
              'res/res_company_view.xml',
              'res/res_partner_view.xml',
              'invoice/account_invoice_view.xml',
              'invoice/account_invoice_line_view.xml',
              'data/account.cee.combined.nomenclature.csv',
              'data/account.cee.service.codes.csv',
              'data/account.cee.nat.of.trans.csv',
              'data/account.cee.way.of.freight.csv',
              'data/account.cee.payment.methods.csv',
              ],
    'demo' : [],
    'active': False,
    'auto_install': True,
    'installable': True
}

