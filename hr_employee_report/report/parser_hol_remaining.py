# -*- coding: utf-8 -*-
##############################################################################
#    
#
##############################################################################
from report import report_sxw
from report.report_sxw import rml_parse
import pooler
import time
from datetime import datetime, timedelta
import copy

class Parser(report_sxw.rml_parse):
    
    
    def __init__(self, cr, uid, name, context):
        #import pdb; pdb.set_trace()
        self.context=context
        self.hols_remaining={}
        self.cr=cr
        self.uid=uid
        self.hol_types=self.get_holidays_type_by_orm(context);
        super(Parser, self).__init__(cr, uid, name, context)
        
        self.localcontext.update({
            'get_emps':self.get_employees,
            'get_date':self.get_date,
            'get_holiday_type':self.get_holiday_type,
            'get_remaining_holidays':self.get_remaining_holidays,
            'get_remaining_holidays_by_type':self.get_remaining_holidays_by_type, 
            'get_desc_holiday_by_type':self.get_desc_holiday_by_type
        })
    
    def get_employees(self):
        #import pdb; pdb.set_trace()
        sql_string_act_ids='''
            select emp.id,res.name
            from hr_employee emp
            inner join resource_resource res on emp.resource_id=res.id
            where res.active=true and emp.department_id is not null
            and emp.id in (%s)
            order by res.name
        '''
        sql_string_no_act_ids='''
            select emp.id,res.name
            from hr_employee emp
            inner join resource_resource res on emp.resource_id=res.id
            where res.active=true and emp.department_id is not null
            order by res.name
        '''
        if(self.context.has_key('active_ids')):
            id_string = ','.join(str(n) for n in self.context['active_ids'])
            sql= sql_string_act_ids % (id_string)
        else:
            sql=sql_string_no_act_ids
        self.cr.execute(sql)
        emps=self.cr.dictfetchall()
        return emps

    def get_holidays_type_by_orm(self,context):
        #hrs=self.pool.get('hr.holidays.status')
        hrs=pooler.get_pool(self.cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(self.cr,self.uid,[])
        orm_types=hrs.read(self.cr,self.uid,hrs_list,['id','name'],context)
        types=[]
        #import pdb; pdb.set_trace()
        for k in orm_types:
            type=[]
            type.append(k['name'])
            type.append(k['id'])
            types.append(type)
        return types

    def get_holiday_type(self):
        return self.hol_types

    def get_remaining_holidays(self,emp_id):
        #hrs=self.pool.get('hr.holidays.status')
        hrs=pooler.get_pool(self.cr.dbname).get('hr.holidays.status')
        hrs_list=hrs.search(self.cr,self.uid,[])
        #self.hol_types=hrss.read(self.cr,self.uid,hrs_list,['id','name'])
        self.hols_remaining=hrs.get_days(self.cr,self.uid,hrs_list,emp_id,0)
        #import pdb; pdb.set_trace()
    
    def get_remaining_holidays_by_type(self,type):
        #import pdb; pdb.set_trace()
        if(self.hols_remaining.has_key(type)):
            return self.hols_remaining[type].values()
        return 0
        
    def get_desc_holiday_by_type(self,type):
        #import pdb; pdb.set_trace()
        if(self.hols_remaining.has_key(type)):
            return self.hols_remaining[type].keys()
        return 0
        
    def get_date(self):
        date=datetime.today()
        return date.strftime("%d %B %Y")
        
        
        
        
        
