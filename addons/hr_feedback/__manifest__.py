# -*- coding: utf-8 -*-
{
    'name': "Interview Feedback",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Module Odoo pour le cours de Développement Web IV.
        Fonctionnalités :
        - Encodage des feedbacks par les employés
        - Gestion des questions et des scores par compétence
        - Intégration avec le module Recrutement
    """,

    'author': "62098 - 63731",
    'website': "https://www.he2b.be",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_recruitment', 'hr_skills'],

    # always loaded
    'data': [
        'security/hr_feedback_rules.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_feedback_views.xml',
        'views/hr_applicant_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True, # Important pour le voir dans les Apps principales
}

