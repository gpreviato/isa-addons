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
from report import report_sxw
from report.report_sxw import rml_parse
from hr_holidays_isa.hr_holidays_isa import hr_holidays_isa as Holidays
import time
from datetime import datetime, timedelta
import pooler
import copy
import locale
from tools.translate import _


def lengthmonth(year, month):
    if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
        return 29
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

class Parser(report_sxw.rml_parse):
    
    
    def __init__(self, cr, uid, name, context):
        self.total_work_hours_4days={}
        self.total_holidays_4days={}
        self.total_holidays={}
        self.totals_by_type={}
        self.totals={}
        self.context=context
        self.holidays_Obj=pooler.get_pool(cr.dbname).get('hr.holidays')
        user=pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid)
        lang=user.context_lang
        locale.setlocale(locale.LC_ALL, str(lang)+".utf8")
        self.hol_type=self._get_holidays_type_by_orm(cr,uid,context)
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_holidays_by_month':self.get_holidays_by_month,
            'get_days':self.get_days,
            'get_holidays_by_type':self.get_holidays_by_type,
            'get_holiday_type':self.get_holiday_type,
            'get_totals_by_type':self.get_totals_by_type,
            'get_date':self.get_date,
            'get_wizard_params':self.get_wizard_params,
            'get_emps':self.get_employees,
        })
    
    def get_employees(self):
        #import pdb; pdb.set_trace()
        sql_string='''
            select emp.id,res.name
            from hr_employee emp
            inner join resource_resource res on emp.resource_id=res.id
            where res.active=true and emp.department_id is not null
            and emp.id in (%s)
            order by res.name
        '''
        id_string = ','.join(str(n) for n in self.context['active_ids'])
        sql= sql_string % (id_string)
        self.cr.execute(sql)
        emps=self.cr.dictfetchall()
        return emps
    
    def get_wizard_params(self,month,year):
        self.month=month
        self.year=year
        
    def get_holidays_by_type(self,hol_type):
        #import pdb; pdb.set_trace()
        if(self.total_holidays.has_key(hol_type)):
            return self.total_holidays[hol_type]
        return 0
        
    def get_totals_by_type(self,hol_type):
        #import pdb; pdb.set_trace()
        return self.totals[hol_type]
    
    
    def _get_holidays_type_by_orm(self,cr,uid,context):
        hrs=pooler.get_pool(cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True)])
        orm_types=hrs.read(cr,uid,hrs_list,['id','name'],context)
        return orm_types
        
        #ritorna le tipologie di permesso che comprendono i festivi,per esempio la malattia
        #It returns the holidays types thath allow destivities days, for example, sick leave        
    def _type_allow_festivities(self,cr,uid,context):
        hrs=pooler.get_pool(cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True),("allow_festivities","=",True)])
        #import pdb; pdb.set_trace()
        return hrs_list
        
        #ritorna le tipologie di permesso che comprendono i giorni di chiusura,per esempio la malattia
        #It returns the holidays types thath allow closed days, for example, sick leave        
    def _type_allow_closed_days(self,cr,uid,context):
        hrs=pooler.get_pool(cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True),("allow_closed_days","=",True)])
        return hrs_list
        
    def get_holiday_type(self):
        return self.hol_type
        
    def get_work_hours_by_month(self,emp_id):
        #~ import pdb; pdb.set_trace()
        last_day_month=lengthmonth(self.year,self.month)
        first_date=datetime(self.year,self.month,1)
        last_date=datetime(self.year,self.month,last_day_month,23,59,59)

        hr_contract_obj = pooler.get_pool(self.cr.dbname).get('hr.contract')
        contract_ids = hr_contract_obj.search(self.cr, self.uid, [('employee_id','=',emp_id),], order='date_start desc')
        if not contract_ids:
             #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a contract'))
             raise Exception(_('The employee does not have a contract'))
             return False
        
        calendar_id = hr_contract_obj.browse(self.cr, self.uid, contract_ids[0]).working_hours.id
        if not calendar_id:
            #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a working hours'))
            raise Exception(_('The employee does not have a working hours'))
            return False
            
        working_range_date=self.holidays_Obj.get_holiday_range_date(self.cr, self.uid, self.context['active_ids'], last_date, first_date, calendar_id)
        #~ import pdb; pdb.set_trace()
        working_range=self.holidays_Obj.get_working_days(self.cr,self.uid,working_range_date)
        working_range_final = {}
        for data_key in sorted(working_range_date):
            working_range_final[data_key] = 0
            if data_key in working_range:
                working_range_final[data_key] = working_range[data_key]
        self.total_work_hours_4days=working_range_final

    def get_holidays_by_month(self,emp_id):
        #import pdb; pdb.set_trace()
        last_day_month=lengthmonth(self.year,self.month)
        first_date=datetime(self.year,self.month,1)
        last_date=datetime(self.year,self.month,last_day_month)
        
        interval=self._get_interval_days(first_date,last_date)
        
        ref_range={}
        for i in interval:
            ref_range[i]=0
        
        tot_range={}
        for k in self._build_totals_dict():
            tot_range[k]=copy.copy(ref_range)
        
        sql = '''
            select hol.number_of_days_temp, hol.holiday_status_id,hol_status.name, hol.holiday_type,
            date_from, date_to
            from hr_employee as emp 
            inner join hr_holidays as hol on emp.id = hol.employee_id
            inner join hr_holidays_status as hol_status on hol_status.id = hol.holiday_status_id
            where hol.type<>'add' 
            and
            (
            (EXTRACT(YEAR FROM (hol.date_from))=%s and 
            EXTRACT(MONTH FROM (hol.date_from))=%s)
            or
            (EXTRACT(YEAR FROM (hol.date_to))=%s and 
            EXTRACT(MONTH FROM (hol.date_to))=%s)
            )
            and emp.id = %s and state='validate'
            order by hol.date_from, hol.holiday_status_id
            '''
           
        #self.cr.execute(sql, (first_date.strftime('%Y-%m-%d %H:%M:%S'), last_date.strftime('%Y-%m-%d %H:%M:%S'), emp_id))
        self.cr.execute(sql, (self.year, self.month,self.year, self.month, emp_id))                
        #variabile da tornare: lista bidimensionale con tutti gli utenti e tutti i giorni.
        managed_holidays=[]
        
        holidays = self.cr.dictfetchall()
        
        for hol in holidays:
            #import pdb; pdb.set_trace()
            
            date_to=datetime.strptime(hol['date_to'],'%Y-%m-%d %H:%M:%S')
            date_from=datetime.strptime(hol['date_from'],'%Y-%m-%d %H:%M:%S')
            """
            hol_interval=self._get_interval_days(datetime.date(date_from),datetime.date(date_to))
            
            hol_range={}
            for i in hol_interval:
                hol_range[i]=0
            """
            
            hr_contract_obj = self.pool.get('hr.contract')
                    
            contract_ids = hr_contract_obj.search(self.cr, self.uid, [('employee_id','=',emp_id),], order='date_start desc')
            if not contract_ids:
                #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a contract'))
                raise Exception(_('The employee does not have a contract'))
                return False
                
            calendar_id = hr_contract_obj.browse(self.cr, self.uid, contract_ids[0]).working_hours.id
            if not calendar_id:
                #raise osv.except_osv(_('Invalid action !'), _('The employee does not have a working hours'))
                raise Exception(_('The employee does not have a working hours'))
                return False
            
            
            hol_range=self.holidays_Obj.get_holiday_range_date(self.cr, self.uid, self.context['active_ids'], date_to, date_from, calendar_id)
            
            #hol_working_range=self._get_working_days(hol_range,hol['holiday_status_id'])
            #import pdb; pdb.set_trace()
            hol_working_range=self.holidays_Obj.get_working_days(self.cr,self.uid,hol_range,hol['holiday_status_id'])
            
            #emp_hol_hours4days = self._get_emp_hol_hours4days(emp_id,float(hol['number_of_days_temp']),hol_working_range)
            emp_hol_hours4days = hol_working_range
            #import pdb; pdb.set_trace()
            for k,v in emp_hol_hours4days.items():
                if (k in tot_range[hol['holiday_status_id']]):
                    tot_range[hol['holiday_status_id']][k] += v
        
        totals=self._build_totals_dict()
        #import pdb; pdb.set_trace()
        total_holidays={}    
        for k in tot_range:
            keys_days=sorted(tot_range[k].keys())
            total_holidays[k]=[]
            for day in keys_days:
                total_holidays[k].append(tot_range[k][day])
                totals[k]+=tot_range[k][day]
        
        self.total_holidays_4days=tot_range
        self.total_holidays=total_holidays
        self.totals=totals
    
    def get_days(self):
        last_day=lengthmonth(self.year,self.month)
        days=[]
        #import pdb; pdb.set_trace()
        for i in range(1,last_day+1,1):
            days.append(i)
        return days
    
    def _build_totals_dict(self):
        totals={}
        holiday_type=self.get_holiday_type()
        for type in holiday_type:
            totals[type['id']]=0
        return totals
    
    def get_date(self):
        date=datetime(self.year,self.month,1)
        return date.strftime("%B %Y")
    
    def _get_interval_days(self,date_from,date_to):
        days=(date_to-date_from).days+1
        interval=[]
        for i in range(days):
            date_act=date_from+timedelta(days=i)
            interval.append(date_act.strftime('%Y-%m-%d'))
        return interval

#ottengo i dati dalla prima company_id derivata dall'utente connesso        
    """    def _get_festivities_orm(self,cr,uid,context):        
            res_tab=pooler.get_pool(cr.dbname).get('resource.resource')
            resource_ids=res_tab.search(cr,uid,[('user_id','=',uid)])                
            resource=res_tab.browse(cr,uid,resource_ids)
            hrs=pooler.get_pool(cr.dbname).get('res.company.festivity')
            #import pdb; pdb.set_trace()
            hrs_list=hrs.search(cr,uid,[("company_id","=",resource[0].company_id.id)])
            orm_types=hrs.read(cr,uid,hrs_list,['day','month','year'],context)
            return orm_types
            
        def _get_closed_days_orm(self,cr,uid,context):        
            res_tab=pooler.get_pool(cr.dbname).get('resource.resource')
            resource_ids=res_tab.search(cr,uid,[('user_id','=',uid)])                
            resource=res_tab.browse(cr,uid,resource_ids)
            hrs=pooler.get_pool(cr.dbname).get('res.company.closed.day')
            hrs_list=hrs.search(cr,uid,[("company_id","=",resource[0].company_id.id)])
            orm_types=hrs.read(cr,uid,hrs_list,['day','hours'],context)
            return orm_types
    """
    """ 
    def _get_working_days(self, range,hol_type):
        import pdb; pdb.set_trace()
        festivities=self.holidays_Obj.get_festivities_orm(self.cr,self.uid)
        closed_days=self.holidays_Obj.get_closed_days_orm(self.cr,self.uid)
                
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
            festivities_date=day+'-'+month+'-'+year
            this_holidays[festivities_date]=1                    
        
        for closed in closed_days:
            day=str(closed['day'])
            hours=str(closed['hours'])            
            this_closed_days[day]=hours                    
            
        new_range={}
        for k in range.keys():
            #east=self._east(self.year)                        
            type_allow_festivities=self._type_allow_festivities(self.cr,self.uid,self.context)                        
            type_allow_closed_days=self._type_allow_closed_days(self.cr,self.uid,self.context)                        
            dt=datetime.strptime(k,'%Y-%m-%d')
            day_included=True
            
            #festivities
            if hol_type in type_allow_festivities:            
                if dt.strftime('%d-%m-%Y') in this_holidays:
                    day_included=False                            
                                        
            #closed days
            #adds 1 unit to the method "weekday()" to fix the bug of Monday=0
            if hol_type in type_allow_closed_days:            
                if str((dt.weekday()+1)) in this_closed_days:
                    #if dt.strftime('%Y-%m-%d') != east:
                    day_included=False            
                        
            if day_included == True:
                new_range[k]=0
        return new_range
    """
    """
    def _get_emp_hol_hours4days(self,emp_id,hol_hours,working_days):
        #import pdb; pdb.set_trace()        
        num_days=len(working_days)
        hol_hours_remaning=hol_hours
        
        for k in working_days.keys():
            hours_for_day=self._getDayOfWeekWorkHours(emp_id,k)            
            working_days[k]=hours_for_day
            hol_hours_remaning=hol_hours_remaning-hours_for_day
        #import pdb; pdb.set_trace()        
        #if hol_hours_remaning>0:
        #   SCEGLIERE COSA FARE IN CASO DI PROBLEMI
        return working_days
    """    
    """    
    def _east(self,year):
      if year<1583 or year>2499: return None
      table={15:(22, 2), 16:(22, 2), 17:(23, 3), 18:(23, 4), 19:(24, 5),
               20:(24, 5), 21:(24, 6), 22:(25, 0), 23:(26, 1), 24:(25, 1)}
      m, n = table[year//100]
      a=year%19
      b=year%4
      c=year%7
      d=(19*a+m)%30
      e=(2*b+4*c+6*d+n)%7
      day=d+e
      if (d+e<10):
        day+=22
        month=3
      else:
        day-=9
        month=4
        if ((day==26) or ((day==25) and (d==28) and (e==6) and (a>10))):
          day-=7
      dt=datetime.strptime(str(year)+"-"+str(month)+"-"+str(day),'%Y-%m-%d')
      return (dt+timedelta(days=1)).strftime('%Y-%m-%d')
    """ 
    """ 
    def _getDayOfWeekWorkHours(self,emp_id,date_day):        
        #import pdb; pdb.set_trace()
        emp_obj=pooler.get_pool(self.cr.dbname).get("hr.employee")
        employee=emp_obj.browse(self.cr,self.uid,emp_id)
        dd=datetime.strptime(date_day,'%Y-%m-%d')
        week_day=dd.weekday()
        calendar_id=employee.resource_id.calendar_id.id
        #day_interval=self._getIntervalliOrariNelGiornodellaSettimana(calendar_id,week_day)
        #import pdb; pdb.set_trace()
        #hr_holidays_isa_obj=hr_holidays_isa()
        day_interval=self._getIntervalliOrariNelGiornodellaSettimana(calendar_id,week_day)
        hours=0
        for interval in day_interval:
            hours=hours+(interval['hour_to']-interval['hour_from'])
        return hours

    def _getIntervalliOrariNelGiornodellaSettimana(self,calendar_id,week_day):
        res_cal_att_obj=pooler.get_pool(self.cr.dbname).get('resource.calendar.attendance')
        calendar_ids=res_cal_att_obj.search(self.cr,self.uid,[('calendar_id','=',calendar_id),('dayofweek','=',str(week_day))])                
        day_interval=[]
        for i in res_cal_att_obj.browse(self.cr,self.uid,calendar_ids):
            day={'hour_from':i.hour_from,'hour_to':i.hour_to}
            day_interval.append(day)
        return day_interval
    """    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
