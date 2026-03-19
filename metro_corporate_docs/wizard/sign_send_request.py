# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import uuid

from odoo import api, fields, models, _


class SignTemplateShare(models.TransientModel):
    _inherit = 'sign.send.request'

    def send_request(self):
        res = self.create_request()
        request = self.env['sign.request'].browse(res['id'])
        corporate_change_address_id = self.env['corporate.address.change'].search([('sign_template_id', '=', request.template_id.id)], limit=1)
        if request and corporate_change_address_id:
            corporate_change_address_id.write({'state': 'signing'})
        return request.go_to_document()
