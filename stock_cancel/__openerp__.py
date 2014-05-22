# -*- encoding: utf-8 -*-
##############################################################################
#
#    Modulo realizzato da Andrea Cometa
#    Compatible with OpenERP release 6.0.0
#    Copyright (C) 2012 Andrea Cometa. All Rights Reserved.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#
##############################################################################
{
	'name': 'Stock Cancel',
	'version': '1.1',
	'category': 'Stock',
	'description': """
	This module allows you to bring back a completed stock picking to draft state
	""",
	'author': 'www.andreacometa.it',
	'website': 'http://www.andreacometa.it',
	'depends': ['stock'],
	'update_xml': [
		'stock_view.xml',
		],
	'installable': True,
	'active': False,
	'images' : ['images/stock_picking.jpg'],
}

