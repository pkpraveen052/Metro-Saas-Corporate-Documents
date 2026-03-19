from odoo import fields, models, api, _
import logging

_logger = logging.getLogger(__name__)


class AddressChangeForm(models.Model):
    _name = "address.change.form"
    _description = "Address Change Form"
    # _rec_name = "business_unit"

    old_address = fields.Text(string='Address')
    new_address = fields.Text(string='New Address')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('document_ready', 'Document Ready'),
        ('document_review', 'Document Review'),
        ('sign', 'Sign'),
        ('ready_to_submit', 'Ready To Submit'),
        ('acra', 'ACRA'),
        ('done', 'Done')
    ], default='draft')
    company_id = fields.Many2one('res.company', string="Company")




