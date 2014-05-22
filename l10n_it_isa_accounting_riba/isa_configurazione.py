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
#           'riba_status': fields.related('distinta_line_ids','riba_line_id','state',
#            type='char', string="Riba State", store=False),
##############################################################################

from osv import fields, osv
from tools.translate import _
class riba_configurazione(osv.osv):
    _inherit = "riba.configurazione"
    _columns = {
        'journal_id':fields.many2one('account.journal', 'Account Riba Payment', required=True),   
 }

riba_configurazione()

