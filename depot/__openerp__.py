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

{
    'name': 'Depot',
    'version': '1.0',
    'author': "ISA srl",
    'website': 'http://www.isa.it',
    'category': 'Tire Dealer/Generic Modules/Depot',
    'description': """This module allows the management of depots.This module is formed by deposits and depot moves of a tire dealer""",
    "depends" : ['report_aeroo_ooo',],
    'init_xml' : [],
    'update_xml': [
        'report/report.xml',
        'wizard/depot_move_tree_filter_view.xml',
        'depot_view.xml',
        ],
    'demo_xml': [],
    'test':[],
    'installable': True,
    'active': False,
    'certificate': '',
}
