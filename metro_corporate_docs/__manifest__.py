# -*- coding: utf-8 -*-

{
    'name': 'Corporate Documents',
    'version': '1.0.1.1',
    'author': 'Metro Group',
    'category': 'All',
    'summary': 'Metro',
    'description': "",
    'website': 'https://metrogroup.solutions/',
    'depends': ['base', 'docx_report_generation', 'mail', 'sign'],
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'data/report.xml',
        'views/address_change_form.xml',
        'views/corp_company_profile.xml',
        'views/officer_detail.xml',
        'views/officer_shareholder_detail.xml',
        'views/menu.xml',
        'views/dashboard.xml',
        'views/address_change.xml',
        'views/corporate_document_attachment.xml',
        'views/template.xml',
        'views/corporate_appointment_secretary.xml',
        'views/corporate_resignation_secretary.xml',
    ],
    "qweb": [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

