# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

#"name" : "eInvoicing & Payments",

{
    "name" : "Account Voucher Ext ISA",
    "version" : "0.1",
    "author" : 'ISA srl',
    'complexity': "normal",
    "description": """
Account Voucher module includes all the basic requirements of Voucher Entries for Bank, Cash, Sales, Purchase, Expanse, Contra, etc.
====================================================================================================================================

    * Voucher Entry
    * Voucher Receipt
    * Cheque Register
    
    OpenERP propose to you automatically the reconciliation of payment amount with the open 
    invoices. This module disable the automatically the reconciliation with credit notes. 
    
    """,
    "category": 'Accounting & Finance Ext ISA',
    "website" : "http://www.isa.it",
    "images" : ["images/customer_payment.jpeg","images/journal_voucher.jpeg","images/sales_receipt.jpeg","images/supplier_voucher.jpeg"],
    "depends" : ["account","account_voucher"],
    "init_xml" : [],

    "demo_xml" : [],

    "update_xml" : ["account_voucher_ext_isa_view.xml"],
    "test" : [      
        "test/account_voucher.yml",
        "test/sales_receipt.yml",
        "test/sales_payment.yml",
        "test/account_voucher_report.yml",
        "test/case1_usd_usd.yml",
        "test/case2_usd_eur_debtor_in_eur.yml",
        "test/case2_usd_eur_debtor_in_usd.yml",
        "test/case3_eur_eur.yml",
        "test/case4_cad_chf.yml",
    ],
    'certificate': '',
    "auto_install": False,
    "application": True,
    "installable": True,
}
