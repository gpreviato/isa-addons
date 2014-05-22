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
from osv import fields,osv
from tools.translate import _
import pooler



class riba_voucher(osv.osv_memory):
    _name = 'riba_wizard_voucher'
    _description = 'Voucher from Riba'
    _columns = {
        'isa_date_riba':fields.date('Date', help="Effective date for riba isa"),
    }

    def create_voucher(self, cr, uid, ids, context=None):
        #import pdb;pdb.set_trace()
        voucher_ids=self.create_draft_voucher(cr,uid,ids,context)
        #account_voucher = pooler.get_pool(cr.dbname).get('account.voucher')        
        #for voucher_id in voucher_ids:
            #step2=account_voucher.proforma_voucher(cr, uid, voucher_id , context)
        return {'type': 'ir.actions.act_window_close'}


    def create_draft_voucher(self, cr, uid, ids, context=None):
        voucher_ids=[]
        riba_voucher_obj = self.pool.get('riba.voucher_isa')
        riba_voucher_isa=riba_voucher_obj.browse(cr, uid, context['active_ids']) 
        account_voucher = self.pool.get('account.voucher')
        #account_voucher = pooler.get_pool(cr.dbname).get('account.voucher')
                
        for riba in riba_voucher_isa:
            #import pdb;pdb.set_trace()
            #creazione testata e righe, ritorno id_testata            
            voucher_id=int(self.isa_account_voucher_create(cr,uid,ids,riba)) 
            voucher_ids.append(voucher_id)
        return voucher_ids

    #metodo per la creazione della testa di account_voucher
    def isa_account_voucher_create(self,cr,uid,ids,riba_voucher):

        #recupero data dal wizard
        values=self.read(cr,uid,ids)
        av_date= values[0]['isa_date_riba']


        #valori_default
        is_multi_currency=True
        account_voucher_type='receipt'
        utente=self.pool.get('res.users').browse(cr,uid,uid)

        #valori da calcolare
        journal_id=riba_voucher.journal_payment_id.id
        account_id=riba_voucher.account_id.id
        partner_id=riba_voucher.partner_id.id
        #move_id=riba_voucher.account_move_line_id
        amount=riba_voucher.amount

        #recupero l'utente per il company_id
        utente=self.pool.get('res.users').browse(cr,uid,uid)
        company_id=utente.company_id.id      #azienda relativa uid

        #recupero il periodo fiscale
        period_pool = self.pool.get('account.period')
        pids = period_pool.find(cr, uid, av_date)
        period_id=pids[0]

        payment_rate_currency_id=1.0
        if riba_voucher.journal_payment_id.currency:
            payment_rate_currency_id=riba_voucher.journal_payment_id.currency.id

        account_voucher_row={
            'payment_rate_currency_id':payment_rate_currency_id
            ,'journal_id':journal_id
            ,'account_id':account_id
            ,'partner_id':partner_id
            ,'is_multi_currency':is_multi_currency
            ,'company_id':company_id
            ,'type':account_voucher_type
            ,'date':av_date
            ,'period_id':period_id
            ,'amount':amount

    }
        #account_voucher_obj = self.pool.get('account.voucher')
        account_voucher_obj = pooler.get_pool(cr.dbname).get('account.voucher')
        #creazione testata
        voucher=account_voucher_obj.create(cr, uid, account_voucher_row)

        #preparazione righe
        voucher_line=account_voucher_obj.recompute_voucher_lines(cr, uid, ids, partner_id, journal_id, 0, False, 'receipt', av_date, None)
        #scrittura righe

        step1=self.isa_voucher_move_line_create(cr, uid, voucher_line,int(voucher),riba_voucher.account_move_line_id,amount)
        return voucher

    #creazione delle righe per voucher
    def isa_voucher_move_line_create(self, cr, uid, voucher_line,voucher_id,account_move_line_id,amount):

        voucher_line_obj=pooler.get_pool(cr.dbname).get('account.voucher.line')
        for line in voucher_line['value']['line_cr_ids']:
            line['voucher_id']=voucher_id
            if line['move_line_id']==account_move_line_id :
                line['reconcile']=True
                line['amount']=amount
            voucher_line_obj.create(cr, uid, line)
        return True


riba_voucher()



