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

class product_category(osv.osv):

	_inherit = "product.category"

	_columns = {
		# ----- Commission for product
		'commission' : fields.float('Commission %'),
	}

product_category()

class product_product(osv.osv):

	_inherit = "product.product"

	_columns = {
		# ----- Commission for category
		'commission' : fields.float('Commission %'),
	}

product_product()
