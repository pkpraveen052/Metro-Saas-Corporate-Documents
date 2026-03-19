# -*- coding: utf-8 -*-
import re

from odoo import fields, models


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


class SignTemplate(models.Model):
    _inherit = "sign.template"

    corporate_address_change_id = fields.Many2one(
        'corporate.address.change',
        string='Address Change',
        copy=False,
        ondelete='set null',
        help='Address Change document that generated this sign template.',
    )


class SignSendRequest(models.TransientModel):
    _inherit = "sign.send.request"

    def _get_director_for_role(self, role_name, directors, assigned_director_ids):
        role_name = (role_name or '').strip()
        if not role_name:
            return False

        director_by_name = directors.filtered(lambda d: d.name and d.name.lower() == role_name.lower())[:1]
        if director_by_name:
            return director_by_name

        role_number_match = re.match(r'^director\s*(\d+)$', role_name, re.IGNORECASE)
        if role_number_match:
            role_number = int(role_number_match.group(1))
            if role_number <= len(directors):
                return directors[role_number - 1]
            return False

        unassigned_directors = directors.filtered(lambda d: d.id not in assigned_director_ids)
        return unassigned_directors[:1]

    def _get_or_create_partner(self, director):
        partner = self.env['res.partner'].search([('email', '=', director.email)], limit=1)
        if partner:
            return partner
        return self.env['res.partner'].create({
            'name': director.name,
            'email': director.email,
        })

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        template_id = defaults.get('template_id')
        signer_defaults = defaults.get('signer_ids')
        if not template_id or not signer_defaults:
            return defaults

        template = self.env['sign.template'].browse(template_id)
        address_change = template.corporate_address_change_id
        if not address_change:
            return defaults

        directors = address_change.officer_ids.filtered(
            lambda officer: officer.position == 'director' and officer.email
        )
        if not directors:
            return defaults

        assigned_director_ids = set()
        updated_signers = []
        for command in signer_defaults:
            if len(command) < 3:
                updated_signers.append(command)
                continue

            signer_values = dict(command[2])
            role = self.env['sign.item.role'].browse(signer_values.get('role_id'))
            director = self._get_director_for_role(role.name, directors, assigned_director_ids)
            if director:
                partner = self._get_or_create_partner(director)
                signer_values['partner_id'] = partner.id
                assigned_director_ids.add(director.id)

            updated_signers.append((command[0], command[1], signer_values))

        defaults['signer_ids'] = updated_signers
        return defaults


