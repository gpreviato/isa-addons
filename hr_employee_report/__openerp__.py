# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

{
	"name" : "report employee",
	"version" : "0.1",
	"description" : "report employee",
	"author" : "ISA srl",
    'website': '',
	"depends" : ["base", "report_aeroo_ooo","hr","hr_overtime","hr_attendance_isa","hr_holidays_isa"],
	"category" : "Generic Modules/Aeroo Reporting",
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : ["report/report.xml",'wizard/hr_summary_bymonth_view.xml','security/ir.model.access.csv'],
	"installable": True
}

