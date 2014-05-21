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

from osv import fields, osv
from tools.translate import _
from datetime import *
from dateutil.rrule import rrule, DAILY
from decimal import *
import sys

class hr_holidays_isa(osv.osv):
    
    _inherit = 'hr.holidays'
    
    _columns = {
        'number_of_days_temp': fields.float('N. Working Hours', readonly=True, states={'draft':[('readonly',False)]}),
    }
    
    _sql_constraints = [
        ('type_value', "CHECK( (holiday_type='employee' AND employee_id IS NOT NULL) or (holiday_type='category' AND category_id IS NOT NULL))", "You have to select an employee or a category"),
        ('date_check', "CHECK ( number_of_days_temp > 0 )", "The number of days must be greater than 0 !"),
        #('date_check', "CHECK ( number_of_days_temp > 0 AND type='remove')", "The number of hours must be greater than 0 !"),
        #('date_check1', "CHECK ( number_of_days_temp <> 0 AND type='add')", "The number of hours must be greater than 0 !"),
        ('date_check2', "CHECK ( (type='add') OR (date_from < date_to))", "The start date must be before the end date !")
    ]

    def holidays_confirm(self, cr, uid, ids, *args):
        record = self.browse(cr, uid, ids)[0]
        if record.date_to and record.date_from :
            
            hr_contract_obj = self.pool.get('hr.contract')
                    
            contract_ids = hr_contract_obj.search(cr, uid, [('employee_id','=',record.employee_id.id),], order='date_start desc')
            if not contract_ids:
                #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a contract'))
                raise Exception(_('The employee does not have a contract'))
                return False
                
            calendar_id = hr_contract_obj.browse(cr, uid, contract_ids[0]).working_hours.id
            if not calendar_id:
                #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a working hours'))
                raise Exception(_('The employee does not have a working hours'))
                return False
        
            date_to=datetime.strptime(record.date_to,'%Y-%m-%d %H:%M:%S').replace(second=0)
            date_from=datetime.strptime(record.date_from,'%Y-%m-%d %H:%M:%S').replace(second=0)
        
            holidays_hours = self._get_holidays_hours(cr, uid, ids, date_to, date_from, record.holiday_status_id.id, calendar_id)
        
            if record.number_of_days_temp <> holidays_hours:
                #raise osv.except_osv(_('Attention !'), _('The number of hours entered manually (%s) are different from those expected (%s)') % (record.number_of_days_temp,holidays_hours))
                raise Exception(_('The number of hours entered manually (%s) are different from those expected (%s)') % (record.number_of_days_temp,holidays_hours))
                return False
        
        res = super(hr_holidays_isa, self).holidays_confirm(cr, uid, ids, *args)
        return res
    
    def onchange_hol_status(self, cr, uid, ids, status,date_to, date_from, employee_id, context=None):
        #import pdb; pdb.set_trace()
        res = super(hr_holidays_isa, self).onchange_sec_id(cr, uid, ids, status, context)
        if res['warning']:
            return res
        else:
            result=self.onchange_date_from(cr, uid, ids, date_to, date_from, status, employee_id)
            return result
    
    def onchange_empl(self, cr, uid, ids, date_to, date_from, holiday_status_id, employee_id):
        result=self.onchange_date_from(cr, uid, ids, date_to, date_from, holiday_status_id, employee_id)
        return result

    def onchange_date_from(self, cr, uid, ids, date_to, date_from, holiday_status_id, employee_id):   
        holidays_hours=0
        if date_to and date_from:
            if not holiday_status_id:
                #raise osv.except_osv(_('Invalid action !'), _('The "Type of holiday" is required'))
                raise Exception(_('The "Type of holiday" is required'))
                return False
                    
            hr_contract_obj = self.pool.get('hr.contract')
            contract_ids = hr_contract_obj.search(cr, uid, [('employee_id','=',employee_id),], order='date_start desc')
            if not contract_ids:
                 #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a contract'))
                 raise Exception(_('The employee does not have a contract'))
                 return False
            
            calendar_id = hr_contract_obj.browse(cr, uid, contract_ids[0]).working_hours.id
            if not calendar_id:
                #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a working hours'))
                raise Exception(_('The employee does not have a working hours'))
                return False
            
            field_date_to=datetime.strptime(date_to,'%Y-%m-%d %H:%M:%S').replace(second=0)
            field_date_from=datetime.strptime(date_from,'%Y-%m-%d %H:%M:%S').replace(second=0)
            
            holidays_hours = self._get_holidays_hours(cr, uid, ids, field_date_to, field_date_from, holiday_status_id, calendar_id)
        
        result = {}
        result['value'] = {
            'number_of_days_temp': holidays_hours,
        }
        return result
        
    def get_holiday_range_date(self,cr,uid,ids,datetime_to,datetime_from,calendar_id):
        holiday_range_dates = {}
        for dt in rrule(DAILY, dtstart=datetime_from.date(), until=datetime_to.date()):
            work_time_intervals_of_weekday = self._get_work_time_intervals_of_weekday(cr, uid, ids, calendar_id, dt.weekday())
            daily_hours = self._get_daily_hours(cr, uid, ids, datetime_to, datetime_from, dt, work_time_intervals_of_weekday)
            holiday_range_dates[dt.strftime('%Y-%m-%d')] = daily_hours
        return holiday_range_dates
        
        
    def _get_holidays_hours(self, cr, uid, ids, datetime_to, datetime_from, hol_type, calendar_id):
        #import pdb; pdb.set_trace()
        holiday_range_dates=self.get_holiday_range_date(cr, uid, ids, datetime_to, datetime_from, calendar_id)
        #elimina festivita o giorni di chiusura
        holiday_range_dates_get_working_days = self.get_working_days(cr, uid, holiday_range_dates, hol_type)
        holidays_hours = 0
        for daily_hours in holiday_range_dates_get_working_days.values():
            holidays_hours = holidays_hours + daily_hours
        return holidays_hours
            
    def _get_work_time_intervals_of_weekday(self, cr, uid, ids, calendar_id,week_day):
        res_cal_att_obj=self.pool.get('resource.calendar.attendance')
        calendar_ids=res_cal_att_obj.search(cr, uid, [('calendar_id','=',calendar_id), ('dayofweek','=',str(week_day))])                
        day_interval=[]
        for i in res_cal_att_obj.browse(cr, uid, calendar_ids):
            day={'hour_from':i.hour_from,'hour_to':i.hour_to}
            day_interval.append(day)
        return day_interval

    def _get_daily_hours(self, cr, uid, ids, datetime_to, datetime_from, date_act, work_time_intervals_of_weekday):
        total_time=timedelta(0)
        for interval in work_time_intervals_of_weekday:
            dt_interval_from = datetime.combine(date_act.date(), self._number_to_time(interval['hour_from']))
            dt_interval_to = datetime.combine(date_act.date(), self._number_to_time(interval['hour_to']))

            if not (datetime_to < dt_interval_from or dt_interval_to < datetime_from): 
                hours_from= max(datetime_from, dt_interval_from)
                hours_to= min(datetime_to, dt_interval_to)
                delta=hours_to-hours_from
                total_time=total_time+delta

        float_time = round((abs(total_time.seconds) / 3600.0),2)
        return float_time

    def _number_to_time(self, numberTime):
        decimalTime= Decimal(str(numberTime))
        decimalHour=decimalTime
        decimalMinute=(decimalTime-int(decimalHour))*60
        decimalSecond=(decimalMinute-int(decimalMinute))*60
        newTime = time(hour = int(decimalHour), minute=int(decimalMinute), second=int(decimalSecond))
        return newTime
        
    def get_working_days(self, cr, uid, range, hol_type = False):
        festivities=self._get_festivities_orm(cr,uid)
        closed_days=self._get_closed_days_orm(cr,uid)
        this_holidays={}
        this_closed_days={}
        
        for festa in festivities:
            day=str(festa['day'])
            month=str(festa['month'])
            year=str(festa['year'])
            if len(day) == 1:
                day='0'+day                
            if len(month) == 1:
                month='0'+month
            festivities_date=year+'-'+month+'-'+day
            this_holidays[festivities_date]=1                    
        
        for closed in closed_days:
            weekday=str(closed['day'])
            hours=closed['hours']            
            this_closed_days[weekday]=hours                    
            
        new_range={}
        #import pdb; pdb.set_trace()        
        for k in range.keys():
            #east=self._east(self.year)                        
            type_allow_festivities=self._type_allow_festivities(cr,uid)                        
            type_allow_closed_days=self._type_allow_closed_days(cr,uid)                        
            dt=datetime.strptime(k,'%Y-%m-%d')
            day_included=True
            
            #festivities
            if hol_type in type_allow_festivities or hol_type == False:            
                if k in this_holidays:
                    day_included=False                            
                                        
            #closed days
            #adds 1 unit to the method "weekday()" to fix the bug of Monday=0
            if hol_type in type_allow_closed_days or hol_type == False:            
                if str((dt.weekday()+1)) in this_closed_days:
                    diff_hours=range[k]-this_closed_days[str(dt.weekday()+1)]
                    if diff_hours > 0:
                        range[k] = diff_hours
                    else:
                        range[k] = 0
                        
            if day_included == True:
                new_range[k]=range[k]
        return new_range
    
    #ottengo i dati dalla prima company_id derivata dall'utente connesso        
    def _get_festivities_orm(self,cr,uid):        
        res_tab=self.pool.get('resource.resource')
        resource_ids=res_tab.search(cr,uid,[('user_id','=',uid)])                
        resource=res_tab.browse(cr,uid,resource_ids)
        hrs=self.pool.get('res.company.festivity')
        #import pdb; pdb.set_trace()
        hrs_list=hrs.search(cr,uid,[("company_id","=",resource[0].company_id.id)])
        orm_types=hrs.read(cr,uid,hrs_list,['day','month','year'])
        return orm_types
        
    def _get_closed_days_orm(self,cr,uid):        
        res_tab=self.pool.get('resource.resource')
        resource_ids=res_tab.search(cr,uid,[('user_id','=',uid)])                
        resource=res_tab.browse(cr,uid,resource_ids)
        hrs=self.pool.get('res.company.closed.day')
        hrs_list=hrs.search(cr,uid,[("company_id","=",resource[0].company_id.id)])
        orm_types=hrs.read(cr,uid,hrs_list,['day','hours'])
        return orm_types
    
    #ritorna le tipologie di permesso che comprendono i giorni di chiusura,per esempio la malattia
    #It returns the holidays types thath allow closed days, for example, sick leave        
    def _type_allow_closed_days(self,cr,uid):
        hrs=self.pool.get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True),("allow_closed_days","=",True)])
        return hrs_list
    
    #ritorna le tipologie di permesso che comprendono i festivi,per esempio la malattia
    #It returns the holidays types thath allow destivities days, for example, sick leave        
    def _type_allow_festivities(self,cr,uid):
        hrs=self.pool.get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True),("allow_festivities","=",True)])
        return hrs_list

hr_holidays_isa()

class hr_holidays_status_isa(osv.osv):
    _inherit = "hr.holidays.status"
    _description = "Leave Type"
    
    _columns = {
        'allow_festivities': fields.boolean('Includes days of festivities', help="If checked, the days of festivities are included in the leave type"),
        'allow_closed_days': fields.boolean('Includes closed days', help="If checked, the closed days are included in the leave type"),
    }

    _defaults = {
        'allow_festivities': False,
        'allow_closed_days': True,
    }
hr_holidays_status_isa()

