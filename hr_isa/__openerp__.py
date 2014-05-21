# -*- coding: utf-8 -*-
##############################################################################
#
##############################################################################

{
    "name": "Human Resources ISA",
    "version": "0.1",
    "author": "ISA srl",
    "category": "Generic Modules/Human Resources",
    "website": "http://www.isa.it",
    "description": """
    HR Customization
    """,
    'depends': ['hr',],
    'init_xml': [],
    'update_xml': [
        'hr_view_isa.xml',
        ],
    'demo_xml': [
        ],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}

