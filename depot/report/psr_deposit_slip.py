# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
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

from datetime import datetime
import time
from report import report_sxw

class Parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_locale_date_from_datetime':self._get_locale_date_from_datetime,
            'get_locale_datetime':self._get_locale_datetime,
        })
        
    def _get_locale_date_from_datetime(self,str_datetime):
        if not str_datetime:
            return False
        locale_date=datetime.strptime(str_datetime,'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        return locale_date
        
    def _get_locale_datetime(self,str_datetime):
        if not str_datetime:
            return False
        locale_datetime=datetime.strptime(str_datetime,'%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M:%S')
        return locale_datetime

    
