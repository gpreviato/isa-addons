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


class salesagent_common(osv.osv):

	_name = "salesagent.common"
	_description = "Generic Utilities"

	# ----- Return the right commission percentuage
	def recognized_commission(self, cr, uid, customer_id, salesagent_id, product_id):
		# If the salesagent field in the order is empty, exit
		commission = 0.0
		if not customer_id or not salesagent_id or not product_id:
			return commission
		partner_product_commission_obj = self.pool.get('partner.product_commission')
		# If customer has a special commission for the product
		lst_commission_product_customer = partner_product_commission_obj.search(cr, uid,
			[('name', '=', product_id), ('partner_id', '=', customer_id)])
		if lst_commission_product_customer:
			commission = partner_product_commission_obj.browse(cr, uid, lst_commission_product_customer[0]).commission
			return commission
		# If customer has a special generic commission
		commission = self.pool.get('res.partner').browse(cr, uid, customer_id).commission
		if commission > 0.0:
			return commission
		# If salesagent has a special commission for the product
		lst_commission_product_customer = partner_product_commission_obj.search(cr, uid,
			[('name', '=', product_id), ('partner_id', '=', salesagent_id)])
		if lst_commission_product_customer:
			commission = partner_product_commission_obj.browse(cr, uid, lst_commission_product_customer[0]).commission
			return commission
		# If product has a special generic commission
		commission = self.pool.get('product.product').browse(cr, uid, product_id).commission
		if commission:
			return commission
		# If salesagent has a special generic commission
		commission = self.pool.get('res.partner').browse(cr, uid, salesagent_id).commission
		return commission

	# ----- Calcola la provvigione totale da riconoscere all'agente
	def commission_calculate(self, cr, uid, param_class, id, context=None):
		'''
		@classe : Indica la classe di riferimento per gli id passati al parametro ids
		@id : id della classe di cui si vuole calcolare la provvigione
		'''
		class_brows = self.pool.get(param_class).browse(cr, uid, id, context)
		total_commission = 0.0
		if param_class == 'account.invoice.line':
			salesagent = class_brows.invoice_id.salesagent_id or False
			customer = class_brows.invoice_id.partner_id
			product = class_brows.product_id or False
			total_price = class_brows.price_subtotal
		percentage_commission = self.recognized_commission(cr, uid, customer and customer.id or False, salesagent and salesagent.id or False, product and product.id or False)
		if percentage_commission:
			total_commission = total_price * percentage_commission
		return total_commission

salesagent_common()
