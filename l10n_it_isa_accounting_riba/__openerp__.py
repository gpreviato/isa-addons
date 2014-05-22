# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 ISA s.r.l. (<http://www.isa.it>).
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
    'name': 'Isa Riba',
    'version': '0.1',
    'category': 'Accounting & Finance"',
    'description': """
            
Gestione e personalizzazione delle Ricevute Bancarie ISA
--------------------------------
Ri.Ba Configurazione
1.Cambiare dicitura etichetta “Importo Accettazione” in “Conto per Accettazione” (verificare PO)

Distinta di presentazione - EMISSIONE RIBA
1.Griglia delle RIBA da emettere: 
    riposizionare la data di scadenza in posizione 1 a sinistra
    ordinare di default la griglia per data scadenza asc
    aggiungere filtro Riba Insolute
2.Filtri Griglia:
    Aggiungere ricerca dalla data alla data di scadenza

3.Distinta di presentazione: una volta confermata l’utente deve avere la possibilità di modificarla e/o eliminarla (funzioni non presenti)

4.All’interno di una distinta: l’utente deve avere la possibilità di modificare o cancellare le singole riba presentate (funzione non presente)

5.Emissione File:

Export file da verificare in home banking 

6.Stampa Distinta di presentazione
    Report di stampa presente in Jasper Report (Tool di stampa sconsigliato da Marzi)
7.Verificare chiusura della partita anche nella visualizzazione delle scadenze di incasso cliente!!

MATURAZIONE – ACCREDITO
1.Aggiungere campo data di accredito prima della registrazione contabile
2.Prevedere checkbox per attivazione “Salta e Conferma Accredito”
3.Eliminazione Registrazione di Accredito
risulta possibile l’eliminazione anche se viene lanciato errore da OE
a seguito dell’eliminazione non cambia lo stato della riba che rimane in “ACCREDITATO”
4.Registrazione di accredito
alla modifica di una riga di un registrazione contabile di accredito OE lancia un errore anche se poi effettua il salvataggio del dato


INSOLUTO
1.se si registra un insoluto riba:
il movimento di riconciliazione contabile non si annulla (viene lanciato errore da OE)
2.eliminazione scrittura di insoluto
alla cancellazione del movimento contabile di insoluto NON CAMBIA LO STATO DELLA RIBA che rimane in stato insoluto
3.alla registrazione di un insoluto (che riapre contabilmente la fattura) 
lo stato della fattura in questione non cambia e resta "PAGATA"!!
       """,
    'author': 'ISA srl',
    'depends': ['l10n_it_ricevute_bancarie',],
    'update_xml': ['isa_accounting_riba.xml',
            'isa_configurazione.xml',
            "wizard/wizard_riba_voucher.xml",
            "isa_riba_vaucher_view.xml",
            ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}
