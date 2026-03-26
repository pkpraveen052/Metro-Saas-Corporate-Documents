from odoo import models, fields, api


class CorpCompanyProfile(models.Model):
    _name = 'corp.company.profile'
    _description = 'Company Profile'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    name = fields.Char("Name of Company")
    uen = fields.Char("UEN")
    company_type = fields.Char("Company Type")
    status = fields.Selection([
        ('live', 'Live'),
        ('inactive', 'Inactive')
    ], string="Company Status")

    incorporation_date = fields.Date("Incorporation Date")
    former_name = fields.Char("Former Name if any")
    name_change_date = fields.Date("Date of Change of Name")

    # Address
    registered_address = fields.Text("Registered Address")
    address_date = fields.Date("Address Updated Date")

    # Compliance
    last_agm_date = fields.Date("Last AGM")
    last_ar_date = fields.Date("Last Annual Return")
    fye_date = fields.Date("Financial Year End")

    # Business Activity
    primary_activity = fields.Char("Primary Activity")
    secondary_activity = fields.Char("Secondary Activity")

    # Capital
    issued_capital = fields.Float("Issued Share Capital")
    paidup_capital = fields.Float("Paid Up Capital")

    # One2many sections
    issued_capital_ids = fields.One2many(
        'corp.company.issued.capital',
        'corp_company_profile_id',
        string="Issued Share Capital"
    )

    paidup_capital_ids = fields.One2many(
        'corp.company.paidup.capital',
        'corp_company_profile_id',
        string="Paid-Up Capital"
    )

    treasury_share_ids = fields.One2many(
        'corp.company.treasury.share',
        'corp_company_profile_id',
        string="Treasury Shares"
    )

    audit_firm_ids = fields.One2many(
        'corp.company.audit.firm',
        'corp_company_profile_id',
        string="Audit Firms"
    )

    charge_ids = fields.One2many(
        'corp.company.charge',
        'corp_company_profile_id',
        string="Charges"
    )

    officer_ids = fields.One2many(
        'corp.company.officer',
        'corp_company_profile_id',
        string="Officers"
    )
    shareholder_ids = fields.One2many(
        'corp.company.shareholder',
        'corp_company_profile_id',
        string="Officers"
    )

    def action_view_officer_shareholder_history(self):
        return {
            'name': 'History',
            'type': 'ir.actions.act_window',
            'res_model': 'corp.officer.shareholder.history',
            'view_mode': 'tree',
        }


class CorpCompanyIssuedCapital(models.Model):
    _name = 'corp.company.issued.capital'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")

    par_value = fields.Float("Amount")
    total_number_share = fields.Integer("Number of Shares")
    currency = fields.Char("Currency")
    share_type = fields.Char("Share Type")


class CorpCompanyPaidupCapital(models.Model):
    _name = 'corp.company.paidup.capital'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")
    total_paidup = fields.Float("Amount")
    total_number_share = fields.Integer("Number of Shares")
    share_type = fields.Char("Share Type")
    currency = fields.Char("Currency")


class CorpCompanyTreasuryShare(models.Model):
    _name = 'corp.company.treasury.share'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")

    number_of_shares = fields.Integer("Number of Shares")
    currency = fields.Char("Currency")


class CorpCompanyAuditFirm(models.Model):
    _name = 'corp.company.audit.firm'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")

    name = fields.Char("Name")

class CorpCompanyCharge(models.Model):
    _name = 'corp.company.charge'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")

    charge_number = fields.Integer("Charge Number")
    charge_date = fields.Date("Date Registered")
    currency = fields.Char("Currency")
    amount_secured = fields.Float("Amount Secured")
    chargee = fields.Char("Chargee(s)")

class CorpCompanyOfficer(models.Model):
    _name = 'corp.company.officer'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")

    email = fields.Char("Email")
    identification_number = fields.Char("Identification Number")
    nationality = fields.Char("Nationality/Citizenship")
    position = fields.Selection([
        ('director', 'DIRECTOR'),
        ('secretary', 'SECRETARY'),
        ('ceo', 'CHIEF EXECUTIVE OFFICER'),
        ('shareholder', 'SHAREHOLDER')
    ], string="Position")
    officer_id = fields.Many2one(
        'officer.detail',
        string="Name"
    )
    appointment_date = fields.Date("Date of Appointment")
    officer_address = fields.Char("Address", related='officer_id.officer_address')

    @api.onchange('officer_id')
    def _onchange_officer_id(self):
        if self.officer_id:
            # self.name = self.officer_id.name
            self.email = self.officer_id.email
            self.identification_number = self.officer_id.identification_number
            self.nationality = self.officer_id.nationality
            self.position = self.officer_id.position
            self.appointment_date = self.officer_id.appointment_date

    def write(self, vals):
        for rec in self:
            self.env['corp.officer.shareholder.history'].create({
                'corp_company_profile_id': rec.corp_company_profile_id.id,
                'officer_id': rec.officer_id.id,
                # 'name': rec.name,
                'identification_number': rec.identification_number,
                'nationality': rec.nationality,
                'position': rec.position,
                'officer_address': rec.officer_address,
            })

        return super().write(vals)

class CorpCompanyShareholder(models.Model):
    _name = 'corp.company.shareholder'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    corp_company_profile_id = fields.Many2one('corp.company.profile', string="Company Profile")
    name = fields.Char("Name")
    identification_number = fields.Char("Identification Number")
    nationality = fields.Char("Nationality/Place of origin")
    total_number_share = fields.Char("Number of Shares")
    currency = fields.Char("Currency")
    shareholder_id = fields.Many2one(
        'officer.detail',
        string="Name"
    )
    officer_address_change = fields.Char("Address Changed")
    shareholder_address = fields.Char("Address", related='shareholder_id.officer_address')

    @api.onchange('shareholder_id')
    def _onchange_officer_id(self):
        if self.shareholder_id:
            self.name = self.shareholder_id.name
            self.identification_number = self.shareholder_id.identification_number
            self.nationality = self.shareholder_id.nationality
            self.total_number_share = self.shareholder_id.total_number_share

    def write(self, vals):
        for rec in self:
            self.env['corp.officer.shareholder.history'].create({
                'corp_company_profile_id': rec.corp_company_profile_id.id,
                'shareholder_id': rec.shareholder_id.id,
                # 'name': rec.name,
                'identification_number': rec.identification_number,
                'nationality': rec.nationality,
                'total_number_share': rec.total_number_share,
                'shareholder_address': rec.shareholder_address,
                'officer_address_change': rec.officer_address_change,
                'currency': rec.currency,
            })

        return super().write(vals)

