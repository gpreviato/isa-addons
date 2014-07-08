# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ISA s.r.l. (<http://www.isa.it>).
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
    'name': "Account Exporter Statements - Lettere d'Intento",
    'version': '0.1',
    'category': 'Accounting & Finance',
    'description': """
Account Exporter Statements - Lettere d'Intento
===============================================

La normativa IVA prevede che i soggetti esportatori abituali che emettono
fatture senza applicazione di imposta possano effettuare i loro acquisti
chiedendo al fornitore di non applicare l'IVA.
In questi casi l'esportatore abituale trasmette al fornitore una
dichiarazione definita “lettera d'intento” in quanto afferma la propria
intenzione di effettuare esportazioni ed il fornitore indicherà gli
estremi della lettera nelle fatture.
La dichiarazione può valere per una singola operazione, per un periodo o
fino a concorrenza di un determinato ammontare.

Le dichiarazioni di intento emesse e ricevute sono memorizzate in una
tabella di database. Per le dichiarazioni ricevute, in fase di
emissione delle fatture verrà applicato il corretto assoggettamento fiscale.


Riepilogo degli adempimenti previsti per i fornitori degli esportatori abituali:

1) La dichiarazione d’intento deve essere annotata, entro 15 giorni,
in un apposito registro o in una sezione del registro delle fatture emesse o dei corrispettivi.

2) Sulla fattura saranno annotati gli estremi della dichiarazione
d’intento ed il titolo di non imponibilità.

3) Entro il 16 del mese successivo a quello di ricevimento della dichiarazione,
deve essere effettuata un’apposita comunicazione in via telematica.
Per la preparazione di questa dichiarazione si vedano le specifiche
tecniche dell'Agenzia delle Entrate riportate in allegato.


    """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it',
    'license': 'AGPL-3',
    'depends' : [
                 'account',
                 'account_financial_report_webkit',
                 'base_fiscalcode',
                 'l10n_it',
                 'report_webkit',
                ],
    'data' : [
              'security/ir.model.access.csv',
              'report/report.xml',
              'wizard/wizard_exporter_statements_view.xml',
              'exporter_statements/account_exporter_statements_view.xml',
        ],
    'demo' : [],
    'installable': True,
    'auto_install': False,
    'certificate': ''
}
