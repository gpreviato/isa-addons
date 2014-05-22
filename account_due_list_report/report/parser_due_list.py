from report import report_sxw
from report.report_sxw import rml_parse
import time
from datetime import datetime, timedelta
import pooler
import copy
import locale
from account.account import account_move_reconcile
from tools.translate import _

class Parser(report_sxw.rml_parse):
    
    
    def __init__(self, cr, uid, name, context):
        #import pdb; pdb.set_trace()
        self.filters=[]
        self.context=context
        user=pooler.get_pool(cr.dbname).get('res.users').browse(cr, uid, uid)
        lang=user.context_lang
        locale.setlocale(locale.LC_ALL, str(lang)+".utf8")
        super(Parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_wizard_params':self.get_wizard_params,
            'get_move_line':self._get_move_line,
            'get_reconcile_name':self.get_reconcile_name,
        })
    
    def get_wizard_params(self,date_from,date_to,partner):
        if date_from :
            f=("date_maturity",">=",date_from)
            self.filters.append(f)
        if date_to :
            t=("date_maturity","<=",date_to)
            self.filters.append(t)
        if partner :
            p=("partner_id","=",partner)
            self.filters.append(p)
        domain=['|','&',('account_id.type','=','payable'),('debit','=',0),'&',('account_id.type','=','receivable'),('credit','=',0)]
        for i in domain:
            self.filters.append(i)
    
    def _get_move_line(self):
        hrs=pooler.get_pool(self.cr.dbname).get('account.move.line')
        hrs_list=hrs.search(self.cr,self.uid,self.filters)
        move_lines=hrs.browse(self.cr,self.uid,hrs_list)
        return move_lines
    
    def get_reconcile_name(self,reconcile_id):
        reconcile_description=''
        if reconcile_id:
            acc=pooler.get_pool(self.cr.dbname).get('account.move.reconcile')
            acc_list=acc.browse(self.cr,self.uid,reconcile_id)
            reconcile_description=acc_list.name_get()[0][1]
            
        return reconcile_description
        
    
