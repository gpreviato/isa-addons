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
import tools
from tools.translate import _

class isa_riba_voucher(osv.osv):
    _name = 'riba.voucher_isa'
    _description = 'Voucher Riba'
    _auto = False

    _columns = {
        'name': fields.char('Reference',size=64),
        'account_move_line_id': fields.integer('Move'),
        'account_id':fields.many2one('account.account', 'Account'),
        'partner_id' :fields.many2one('res.partner', "Cliente"),
        'journal_payment_id':fields.many2one('account.journal', "Journal"),
        'distinta_id':fields.integer('distinta'),
        'date_due': fields.date('Due Date'),
        'date': fields.date('Date'),
        'amount': fields.float('Amount'),


    }
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'riba_voucher_isa')
        cr.execute("""
            CREATE OR REPLACE view riba_voucher_isa as(
                SELECT  
                    aml.id as id
                    ,aml.ref as name
                    ,rd.id as distinta_id
                    ,rdl.partner_id as partner_id
                    ,aml.debit as amount
                    ,aml.date_maturity as date_due
                    ,aml.date
                    ,aml.id as account_move_line_id
                    ,aml.account_id as account_id
                    ,rc.journal_id as journal_payment_id
                    from account_move_line aml
                    left join riba_distinta_line rdl 
	                    on aml.move_id=rdl.acceptance_move_id
                    left join riba_distinta rd 
	                    on rd.id=rdl.distinta_id
                    left join riba_configurazione rc 
	                    on rc.id=rd.config
                    where aml.journal_id in (select accreditation_journal_id from riba_configurazione)
                    AND aml.reconcile_id is null
                    AND aml.tax_code_id is null
                    AND aml.date_maturity is not null)
        """)


isa_riba_voucher()
