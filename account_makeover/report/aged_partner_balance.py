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

import os
from openerp.report import report_sxw
# from openerp.addons.account.report.common_report_header import common_report_header
from openerp.addons.account.report.account_aged_partner_balance import aged_trial_report

class parser_aged_trial_report(aged_trial_report):
     
    def __init__(self, cr, uid, name, context):
        aged_trial_report.__init__(self, cr, uid, name, context=context)

report_sxw.report_sxw('report.makeover.aged.trial.balance', 'res.partner',
                      os.path.dirname(os.path.realpath(__file__)) + '/aged_partner_balance.rml', parser=parser_aged_trial_report, header="internal landscape")
