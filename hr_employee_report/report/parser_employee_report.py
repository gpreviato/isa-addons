# -*- coding: utf-8 -*-
##############################################################################
#    
#
##############################################################################
from report import report_sxw
from report.report_sxw import rml_parse
import time
from datetime import datetime, timedelta
from hr_holidays_isa.report.parser_holidays import Parser as Holidays
from hr_overtime.report.parser_overtime import Parser as Overtime
from hr_attendance_isa.report.parser_attendances import Parser as Attendances
import pooler
import copy
import locale

def lengthmonth(year, month):
    if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
        return 29
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

class Parser(report_sxw.rml_parse):
    
    
    def __init__(self, cr, uid, name, context):
        self.total_holidays={}
        self.totals_by_type={}
        self.totals={}
        #import pdb; pdb.set_trace()
        self.context=context
        
        self.p_att=Attendances(cr, uid, name, context)
        self.p_overt=Overtime(cr, uid, name, context)
        self.p_holy=Holidays(cr, uid, name, context)
        
        user=pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid)
        lang=user.context_lang
        locale.setlocale(locale.LC_ALL, str(lang)+".utf8")
        
        
        #import pdb; pdb.set_trace()
        self.hol_type=self._get_holidays_type_by_orm(cr,uid,context)
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_holidays_by_month':self.p_holy.get_holidays_by_month,
            'get_days':self.get_days,
            'get_holidays_by_type':self.p_holy.get_holidays_by_type,
            'get_holiday_type':self.p_holy.get_holiday_type,
            'get_totals_by_type':self.p_holy.get_totals_by_type,
            'get_date':self.get_date,
            'get_wizard_params':self.get_wizard_params,
            'get_emps':self.get_employees,
            'get_all_attendances':self.p_att.get_total_attendance,
            'get_attendances':self.p_att.get_day_attendance,
            'get_total_att':self.p_att.get_total,
            'get_overtime_by_month':self.p_overt.get_overtime_by_month,
            'get_overtime_by_type':self.p_overt.get_overtime_by_type,
            'get_totals_ot_by_type':self.p_overt.get_totals_by_type,
            'get_overtime_type':self.p_overt.get_overtime_type,
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
        self.p_att.get_wizard_params(month,year)
        self.p_overt.get_wizard_params(month,year)
        self.p_holy.get_wizard_params(month,year)
    
    def _get_holidays_type_by_orm(self,cr,uid,context):
        hrs=pooler.get_pool(cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(cr,uid,[("active","=",True)])
        orm_types=hrs.read(cr,uid,hrs_list,['id','name'],context)
        return orm_types        
        
    def get_holiday_type(self):
        return self.hol_type        
    
    def get_days(self):
        last_day=lengthmonth(self.year,self.month)
        days=[]
        #import pdb; pdb.set_trace()
        for i in range(1,last_day+1,1):
            days.append(i)
        return days
        
    def get_date(self):
        date=datetime(self.year,self.month,1)
        return date.strftime("%B %Y")
