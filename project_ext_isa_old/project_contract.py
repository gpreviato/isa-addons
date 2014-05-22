# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 ISA s.r.l. (<http://www.isa.it>).
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



class project_isa_contract(osv.osv):
    _description = 'Contract of Isa project'
    _name = 'project.contract'
    
    _columns = {
        'name': fields.char('Description', size=255, required=True, select=True),
        'partner_id': fields.many2one('res.partner', 'Partner',required=True),
        'contract_number':fields.char('Contract Number', size=6, required=True),
        'lines': fields.one2many('project.contract.line', 'contract_id'),
        #'contract_line': fields.many2one('project.contract.line', 'Project_contract_line'),
        'project_ids': fields.many2one('project.project', 'project_id'),
    }
    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for item in self.browse(cr, uid, ids, context=context):
            item_desc = item.contract_number and item.contract_number + ' - ' or ''
            item_desc += item.name
            res.append((item.id,item_desc))
        return res

project_isa_contract()

class users(osv.osv):
    _inherit = 'res.users'
    _columns = {
        'context_project_contract_id': fields.many2one('project.contract', 'Project_contract'),
    }
users()

class project_isa_contract_line(osv.osv):
    _description = 'Contract line of Isa project'
    _name = 'project.contract.line'
    
    _columns = {
        'name': fields.char('Description', size=255, required=True, select=True),
        'contract_id': fields.many2one('project.contract', 'Contract', required=True),
        'contract_line_number':fields.char('Contract Line Number', size=6, required=True),
        'project_ids': fields.many2one('project.project', 'project_id'),
    }

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        res = []
        for item in self.browse(cr, uid, ids, context=context):
            item_desc = item.contract_line_number and item.contract_line_number + ' - ' or ''
            item_desc += item.name
            res.append((item.id,item_desc))
        return res

project_isa_contract_line()


