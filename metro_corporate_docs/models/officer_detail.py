from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)


class OfficerDetail(models.Model):
    _name = 'officer.detail'
    _description = 'Officer Detail'

    name = fields.Char("Officer Name", required=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    identification_number = fields.Char("Identification Number")
    email = fields.Char("Email")
    nationality = fields.Char("Nationality/Citizenship")
    position = fields.Selection([
        ('director', 'DIRECTOR'),
        ('secretary', 'SECRETARY'),
        ('ceo', 'CHIEF EXECUTIVE OFFICER'),
        ('shareholder', 'SHAREHOLDER')
    ], string="Position")
    appointment_date = fields.Date("Date of Appointment")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    officer_address = fields.Char("Address", compute="_compute_officer_address")
    total_number_share = fields.Char("Number of Shares/Currency")


    @api.depends('street', 'street2', 'city', 'state_id', 'zip', 'country_id')
    def _compute_officer_address(self):
        for rec in self:
            address = []

            if rec.street:
                address.append(rec.street)
            if rec.street2:
                address.append(rec.street2)
            if rec.city:
                address.append(rec.city)
            if rec.state_id:
                address.append(rec.state_id.name)
            if rec.zip:
                address.append(rec.zip)
            if rec.country_id:
                address.append(rec.country_id.name)

            rec.officer_address = ', '.join(address)



