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


class CorporateResignationSecretary(models.Model):
    _name = 'corporate.resignation.secretary'
    _rec_name = 'company_uen'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    company_id = fields.Many2one('res.company', string='Select Company', required=True, tracking=True, domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)])
    date = fields.Date("Date", default=date.today(), tracking=True, required=True)
    company_uen = fields.Char(string='Company UEN', tracking=True, required=True)
    address = fields.Text(string='Address')
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
    # corp_doc_attach_ids = fields.Many2many('corporate.document.attachment', string='Sign Template')
    secretary_id = fields.Many2one('officer.detail', string='Secretary')


    @api.onchange('company_id')
    def _onchange_company_id(self):
        for rec in self:
            address = []
            if rec.company_id:
                company = rec.company_id
                rec.company_uen = rec.company_id.l10n_sg_unique_entity_number or ''
                if company.street:
                    address.append(company.street)
                if company.street2:
                    address.append(company.street2)
                if company.city:
                    address.append(company.city)
                if company.state_id:
                    address.append(company.state_id.name)
                if company.zip:
                    address.append(company.zip)
                if company.country_id:
                    address.append(company.country_id.name)

                rec.address = ', '.join(address)


    @api.model
    def create(self, vals):
        vals['state'] = 'review'
        return super(CorporateResignationSecretary, self).create(vals)

    def action_print_docx(self):
        log = _("<b>Document downloaded successfully!</b>")
        self.message_post(body=log)
        return self.env.ref('metro_corporate_docs.ir_actions_report_corporate_address_change').report_action(self)

    def action_print_pdf(self):
        log = _("<b>PDF document downloaded successfully!</b>")
        self.message_post(body=log)
        return self.env.ref(
            'metro_corporate_docs.ir_actions_report_corporate_address_change_pdf'
        ).report_action(self)

    def get_effective_date(self):
        def get_ordinal_suffix(day):
            if 11 <= day <= 13:
                return 'th'
            last_digit = day % 10
            if last_digit == 1:
                return 'st'
            elif last_digit == 2:
                return 'nd'
            elif last_digit == 3:
                return 'rd'
            else:
                return 'th'

        def get_date_string():
            now = self.effective_date
            day = now.day
            month = now.strftime("%B")
            year = now.year
            ordinal_suffix = get_ordinal_suffix(day)
            return f"{day}{ordinal_suffix} {month} {year}"

        formatted_date = get_date_string()

        return formatted_date

    def get_passedon_date(self):
        formatted_date = self.passed_on_date.strftime("%d/%m/%Y")
        return formatted_date

    def get_current_date(self):
        formatted_date = datetime.now().strftime("%d/%m/%Y")
        return formatted_date

    def get_company_address(self):
        address = ""
        if self.company_id.street:
            address += self.company_id.street + " "
        if self.company_id.street2:
            address += self.company_id.street2 + " "
        if self.company_id.city:
            address += self.company_id.city + " "
        if self.company_id.country_id:
            address += self.company_id.country_id.name + " "
        if self.company_id.zip:
            address += f"({self.company_id.zip})"
        return address

    def get_current_date1(self):
        def get_ordinal_suffix(day):
            if 11 <= day <= 13:
                return 'th'
            last_digit = day % 10
            if last_digit == 1:
                return 'st'
            elif last_digit == 2:
                return 'nd'
            elif last_digit == 3:
                return 'rd'
            else:
                return 'th'

        def get_current_date_string():
            now = datetime.now()
            day = now.day
            month = now.strftime("%B")
            year = now.year
            ordinal_suffix = get_ordinal_suffix(day)
            return f"{day}{ordinal_suffix} {month} {year}"

        current_date_string = get_current_date_string()
        return current_date_string

    def get_directors_block(self):
        directors = self.officer_ids.filtered(
            lambda x: x.position == 'director'
        )
        result = ""
        for d in directors:
            result += "\n\n_________________________\n"
            result += "%s\nDIRECTOR\n" % d.officer_id.name
        return result

    # def get_director_1(self):
    #     names = self.get_director_names()
    #     return names[0] if len(names) > 0 else ''
    #
    # def get_director_2(self):
    #     names = self.get_director_names()
    #     return names[1] if len(names) > 1 else ''
    #
    # def get_director_3(self):
    #     names = self.get_director_names()
    #     return names[2] if len(names) > 2 else ''

    def action_draft(self):
        self.write({'state': 'draft'})

    import base64
    import tempfile
    import subprocess
    import os

    def action_review(self):
        self.ensure_one()

        report = self.env.ref(
            'metro_corporate_docs.ir_actions_report_corporate_address_change'
        )

        # Generate DOCX
        docx_content, _ = report._render(self.ids)

        # Convert to PDF
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            f.write(docx_content)
            docx_path = f.name

        pdf_path = docx_path.replace('.docx', '.pdf')

        subprocess.call([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(docx_path),
            docx_path
        ])

        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Address_Change_1%s.pdf' % self.company_id.name,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })
        if attachment:
            self.write({'state': 'pre_sign_check'})
            self.env.cr.commit()
        print('\n\n\n\nattachmentattachment', attachment)

        # Cleanup
        try:
            os.remove(docx_path)
            os.remove(pdf_path)
        except:
            pass

        # 🔥 RETURN PREVIEW ACTION
        return {
            'type': 'ir.actions.client',
            'tag': 'corporate_view_report_pdf',
            'params': {
                'attachment_id': attachment.id,
                'res_id': self.id,
                'model': self._name,
            }
        }

    def action_signing(self):
        self.ensure_one()
        report = self.env.ref(
            'metro_corporate_docs.ir_actions_report_corporate_address_change'
        )

        # STEP 1: generate DOCX
        docx_content, _ = report._render(self.ids)

        # STEP 2: convert to PDF
        import tempfile, subprocess, os

        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as f:
            f.write(docx_content)
            docx_path = f.name

        pdf_path = docx_path.replace('.docx', '.pdf')

        subprocess.call([
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', os.path.dirname(docx_path),
            docx_path
        ])

        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()

        # STEP 3: attach PDF

        attachment = self.env['ir.attachment'].create({
            'name': 'Address_Change_%s.pdf' % self.company_id.name,
            'type': 'binary',
            'datas': base64.b64encode(pdf_content),
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf',
        })

        self.message_post(
            body="Signed PDF generated.",
            attachment_ids=[attachment.id]
        )
        template = self.env['sign.template'].create({
            'name': 'Address_Change_%s' % self.company_id.name,
            'attachment_id': attachment.id,
        })
        if template:
            self.sign_template_id = template.id
        return {
            'type': 'ir.actions.client',
            'tag': 'sign.Template',
            'name': 'Sign Document',
            'context': {
                'id': template.id,
            },
            'params': {
                'id': template.id,
            }
        }

    def open_requests(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Sign requests"),
            "res_model": "sign.request",
            "view_mode": "tree,form",
            "domain": [("template_id", "=", self.sign_template_id.id)],
            "context": {'search_default_signed': True},
        }

    def action_create_dynamic_fields(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Custom Dynamic Fields',
            'res_model': 'dynamic.fields',
            'view_mode': 'form',
            'target': 'new',  # ✅ Popup
            'context': {
                'default_model_id': self.env['ir.model']._get_id('corporate.resignation.secretary'),
                'default_model_name': self._name,
            }
        }

    def get_company_full_address(self):
        self.ensure_one()
        company = self.company_id
        return "%s\n%s\n%s %s" % (
            company.street or '',
            company.street2 or '',
            company.country_id.name or '',
            company.zip or ''
        )