# -*- encoding: utf-8 -*-
##############################################################################
##############################################################################

{
    "name" : "Account Payment Type",
    "version" : "0.1",
    "author" : "ISA srl",
    "category" : "Generic Modules/Accounting",
    "website" : "www.isa.it",
    "license" : "AGPL-3",
    "description": """Account Payment type.

This module extends the account_payment module, adding Payment Type
""",
    "depends" : [
        "base",
        "account",
        "account_payment",
        ],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        "payment_view.xml",
        "payment_sequence.xml",
        "security/ir.model.access.csv",
        ],
    "active": False,
    "installable": True,
}

