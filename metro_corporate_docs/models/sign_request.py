# -*- coding: utf-8 -*-
from sympy import limit

from odoo import api, fields, models, _
import datetime
from datetime import datetime, date
import string
import subprocess
import os
import base64




class SignRequest(models.Model):
    _inherit = "sign.request"

    def write(self, vals):
        res = super().write(vals)
        print('\n\n\nvalsvals>>>>>>>>', vals)
        if 'state' in vals and vals['state'] == 'signed':
            for rec in self.env['corporate.address.change'].search([('sign_template_id', '=', self.template_id.id)], limit=1):
                if rec:
                    rec.state = 'sign_finished'

        return res




