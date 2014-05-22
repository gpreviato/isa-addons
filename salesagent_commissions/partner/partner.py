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

class res_partner(osv.osv):

	_inherit = "res.partner"

	_columns = {
		'salesagent' : fields.boolean("Salesagent"),
		# ----- Relation with customers
		'customer_for_salesagent_ids' : fields.one2many('res.partner', 'salesagent_for_customer_id', 'Customers', readonly=True),
		# ----- Relation with salesagent
		'salesagent_for_customer_id': fields.many2one('res.partner', 'Salesagent'),
		# ----- General commission for salesagent
		'commission' : fields.float('Commission %'),
		'product_provvigioni_ids' : fields.one2many('partner.product_commission', 'partner_id', 'Commission for products'),
	}

res_partner()

class partner_product_commission(osv.osv):

	_name = "partner.product_commission"
	_description = "Relation for Partner, products and commissions"

	_columns = {
		'name' : fields.many2one('product.product', 'Product'),
		'commission' : fields.float('Commission'),
		'partner_id' : fields.many2one('res.partner', 'Partner'),
		}

partner_product_commission()
