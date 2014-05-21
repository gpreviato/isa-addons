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
        #import pdb; pdb.set_trace()
        self.filters=[]
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'get_wizard_params':self._get_wizard_params,
            'get_depot_moves':self._get_depot_moves,
            'get_locale_date_from_datetime':self._get_locale_date_from_datetime,
            'get_locale_datetime':self._get_locale_datetime,
        })
    
    def _get_wizard_params(self,form_values):
        #import pdb; pdb.set_trace()
        if form_values['depot_id'] :
            depot_id=form_values['depot_id']
            filter=("depot_id","=",depot_id)
            self.filters.append(filter)
        if form_values['date_storage_from'] :
            date_storage_from=form_values['date_storage_from']
            filter=("date_storage",">=",date_storage_from)
            self.filters.append(filter)
        if form_values['date_storage_to'] :
            date_storage_to=form_values['date_storage_to']
            filter=("date_storage","<=",date_storage_to)
            self.filters.append(filter)
        if form_values['date_pickup_from'] :
            date_pickup_from=form_values['date_pickup_from']
            filter=("date_pickup",">=",date_pickup_from)
            self.filters.append(filter)
        if form_values['date_pickup_to'] :
            date_pickup_to=form_values['date_pickup_to']
            filter=("date_pickup","<=",date_pickup_to)
            self.filters.append(filter)
        if form_values['date_pickup_scheduled_from'] :
            date_pickup_scheduled_from=form_values['date_pickup_scheduled_from']
            filter=("date_pickup_scheduled",">=",date_pickup_scheduled_from)
            self.filters.append(filter)
        if form_values['date_pickup_scheduled_to'] :
            date_pickup_scheduled_to=form_values['date_pickup_scheduled_to']
            filter=("date_pickup_scheduled","<=",date_pickup_scheduled_to)
            self.filters.append(filter)
            
    def _get_depot_moves(self):
        #import pdb; pdb.set_trace()
        report_model=self.localcontext['data']['model']
        report_obj=self.pool.get(report_model)
        line_ids=report_obj.search(self.cr,self.uid,self.filters)
        report_lines=report_obj.browse(self.cr,self.uid,line_ids)
        return report_lines
    
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
    
