# -*- encoding: utf-8 -*-
##############################################################################
##############################################################################

import netsvc
from openerp.osv import fields, osv

class account_invoice(osv.osv):
    _inherit='account.invoice'
    _columns={
        'payment_type': fields.many2one('payment.type', 'Payment type'),
    }

    def onchange_partner_id(self, cr, uid, ids, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        # Copy partner data to invoice, also the new field payment_type
        result = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)
        payment_type = False
        if partner_id:
            partner_line = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if partner_line:
                if type=='in_invoice' or type=='in_refund':
                    payment_type = partner_line.payment_type_supplier.id
                else:
                    payment_type = partner_line.payment_type_customer.id
            if payment_type:
                result['value']['payment_type'] = payment_type
        return self.onchange_payment_type(cr, uid, ids, payment_type, partner_id, result)

    def onchange_payment_type(self, cr, uid, ids, payment_type, partner_id, result = None):
        if result is None:
            result = {'value': {}}
        if payment_type and partner_id:
            bank_types = self.pool.get('payment.type').browse(cr, uid, payment_type).suitable_bank_types
            if bank_types: # If the payment type is related with a bank account
                bank_types = [bt.code for bt in bank_types]
                partner_bank_obj = self.pool.get('res.partner.bank')
                args = [('partner_id', '=', partner_id), ('default_bank', '=', 1), ('state', 'in', bank_types)]
                bank_account_id = partner_bank_obj.search(cr, uid, args)
                if bank_account_id:
                    result['value']['partner_bank_id'] = bank_account_id[0]
                    return result
        result['value']['partner_bank_id'] = False
        return result
account_invoice()
