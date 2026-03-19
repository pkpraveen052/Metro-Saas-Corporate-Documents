from odoo import models, fields

class CorpOfficerShareholderHistory(models.Model):
    _name = 'corp.officer.shareholder.history'
    _description = 'Officer / Shareholder History'

    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company")
    position = fields.Selection([
        ('director', 'DIRECTOR'),
        ('secretary', 'SECRETARY'),
        ('ceo', 'CHIEF EXECUTIVE OFFICER'),
        ('shareholder', 'SHAREHOLDER')
    ], string="Position")
    name = fields.Char("Name")
    shareholder_id = fields.Many2one(
        'officer.detail',
        string="Name"
    )
    officer_id = fields.Many2one(
        'officer.detail',
        string="Name"
    )
    identification_number = fields.Char("Identification Number")
    nationality = fields.Char("Nationality")
    position = fields.Selection([
        ('director', 'DIRECTOR'),
        ('secretary', 'SECRETARY'),
        ('ceo', 'CHIEF EXECUTIVE OFFICER'),
        ('shareholder', 'SHAREHOLDER')
    ])
    total_number_share = fields.Char("Shares")
    officer_address_change = fields.Char("Address Changed")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    change_date = fields.Datetime("Change Date", default=fields.Datetime.now)
    officer_address = fields.Char("Address", related='officer_id.officer_address')
    shareholder_address = fields.Char("Address", related='shareholder_id.officer_address')
    currency = fields.Char("Currency")
