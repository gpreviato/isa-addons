# -*- encoding: utf-8 -*-
##############################################################################
#
#    Modulo realizzato da Apruzzese Francesco
#    Compatible with OpenERP release 6.0.0
#    Copyright (C) 2010 Andrea Cometa. All Rights Reserved.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#
##############################################################################


from osv import fields, osv
import time


class account_invoice(osv.osv):

	_inherit = "account.invoice"

	def create(self, cr, uid, vals, context=None):
		invoice_id = super(account_invoice, self).create(cr, uid, vals, context)
		# QUI DOVRA RICHIAMARE L?AGENTE PARTENDO DAL CLIENTE
		#partner = self.pool.get('res.partner').read(cr, uid, partner_id, ['salesagent_for_customer_id'])
		#agente_id = partner['salesagent_for_customer_id']
		return invoice_id

	def _total_commission(self, cr, uid, ids, name, arg, context=None):
		res = {}
		for invoice in self.browse(cr, uid, ids, context=context):
			total_commission = 0.0 
			for line in invoice.invoice_line:
				total_commission += line.commission
			res[invoice.id] = total_commission
		return res

	def onchange_partner_id(self, cr, uid, ids, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
		if not partner_id:
			return {}
		partner = self.pool.get('res.partner').read(cr, uid, partner_id, ['salesagent_for_customer_id'])
		salesagent_id = partner['salesagent_for_customer_id']
		res = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)
		res['value']['salesagent_id'] = salesagent_id
		return res

	_columns = {
		'salesagent_id' : fields.many2one('res.partner', 'Salesagent'),
		'commission' : fields.function(_total_commission, method=True, string='Commission', type='float', store=False),
		'paid_commission' : fields.boolean('Paid'),
		'paid_date' : fields.date('Commission Payment Date'),
	}

account_invoice()


class account_invoice_line(osv.osv):

	_inherit = "account.invoice.line"

	def _commission(self, cr, uid, ids, name, arg, context=None):
		res = {}
		salesagent_common_obj = self.pool.get('salesagent.common')
		for line in self.browse(cr, uid, ids, context=context):
			res[line.id] = {'commission':0.0, 'commission_percentage':0.0}
			if not line.no_commission:
				# ----- if a paid commission exist, show it or calculate it
				if line.paid_commission_value:
					comm = line.paid_commission_value
					comm_percentage = line.paid_commission_percentage_value
				else:
					comm = salesagent_common_obj.commission_calculate(cr, uid, 'account.invoice.line', line.id)
					comm_percentage = salesagent_common_obj.recognized_commission(cr, uid, line.partner_id and line.partner_id.id or False, line.salesagent_id and line.salesagent_id.id or False, line.product_id and line.product_id.id or False)
				res[line.id]['commission'] = comm
				res[line.id]['commission_percentage'] = comm_percentage
				if comm > 0:
					self.write(cr, uid, [line.id, ], {'commission_presence':True})
				else:
					self.write(cr, uid, [line.id, ], {'commission_presence':False})
			else:
				self.write(cr, uid, [line.id, ], {'commission_presence':False})
		return res

	_columns = {
		'no_commission' : fields.boolean('No Commission', help='Indicates if the commission __ NOT__ must be calculated for this time!'),
		'commission_presence' : fields.boolean('Commission Presence'),
		'commission_percentage' : fields.function(_commission, method=True, string='Comm. Percentage', type='float', store=False, multi='comm'),
		'commission' : fields.function(_commission, method=True, string='Provv. Total', type='float', store=False, multi='comm'),
		'salesagent_id' : fields.related('invoice_id', 'salesagent_id', type='many2one', relation='res.partner', string='Salesagent',
			store=False),
		'partner_id' : fields.related('invoice_id', 'partner_id', type='many2one', relation='res.partner', string='Customer', store=True),
		'date_invoice' : fields.related('invoice_id', 'date_invoice', type='date', string='Invoice Date',
			store=False),
		'paid_commission_value' : fields.float('Paid Commission'),
		'paid_commission_percentage_value' : fields.float('Paid Commission Percentage'),
		'paid_commission' : fields.boolean('Paid'),
		'payment_commission_date' : fields.date('Payment Commission Date'),
		'payment_commission_note' : fields.char('Payment Commission Note', size=128),
	}

	_defaults = {
		'no_commission' : False,
		'paid_commission_value' : 0.0,
		}

account_invoice_line()
