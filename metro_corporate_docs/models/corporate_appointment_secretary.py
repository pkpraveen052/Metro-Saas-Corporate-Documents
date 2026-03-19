# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models, _
import datetime
from datetime import datetime, date
import string
import subprocess
import os
import base64
import tempfile
import subprocess
import os
import base64


class CorporateAppointmentSecretary(models.Model):
    _name = 'corporate.appointment.secretary'
    _rec_name = 'company_uen'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', string='Select Company', required=True, tracking=True, domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)])
    company_name = fields.Char(string='Company', tracking=True)
    passed_on_date = fields.Date("Date", default=date.today(), tracking=True, required=True)
    company_uen = fields.Char(string='Company UEN', tracking=True, required=True)
    old_address = fields.Text(string='Old Address', related='corp_company_profile_id.registered_address')
    new_address = fields.Text(string='New Address')
    corp_company_profile_id = fields.Many2one('corp.company.profile', string='Company Profile')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Review'),
        ('pre_sign_check', 'Pre sign check'),
        ('signing', 'Signing'),
        ('sign_finished', 'Sign finished'),
        ('acra', 'ACRA(Manually)'),
        ('done', 'Done')
    ], default='draft')

    sign_template_id = fields.Many2one('sign.template', string='Sign Template')
    corp_doc_attach_ids = fields.Many2many('corporate.document.attachment', string='Sign Template')

    appointed_person = fields.Char("Appointed Person", tracking=True)
    effective_date = fields.Date('Effective Date', default=date.today(), tracking=True)
    prepared_by = fields.Char('Prepared By', default=lambda self: self.env.user.name, tracking=True)
    role = fields.Char('Role', default='Director', tracking=True)
    type_of_doc = fields.Char(default='DPO Document', string='Type of Doc')
    is_send_sign = fields.Boolean('Send Sing', default=False)