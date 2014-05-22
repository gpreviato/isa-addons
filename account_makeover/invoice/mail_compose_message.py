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

from openerp.osv import orm

"""
    FIX: E'stata ridefinita la funzione 'onchange_template_id' della classe
    'mail_compose_message' per evitare il bug: 
    
        "QWebTemplateNotFound: External ID not found in the system: account.invoice" 
    
    che si verifica nella generazione di una email in 
    
        "CONTABILITA' -> Fatture clienti -> Fattura# -> Invia per email"    
"""

class mail_compose_message(orm.TransientModel):
    _inherit = 'mail.compose.message'
    
    def onchange_template_id(self, cr, uid, ids, template_id, composition_mode, model, res_id, context=None):            
            return {'value': []}