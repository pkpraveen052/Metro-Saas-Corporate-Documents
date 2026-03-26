# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MetroCorporateDocsDashboard(models.TransientModel):
    _name = 'metro.corporate.docs.dashboard'
    _description = 'Corporate Documents Dashboard'

    address_change_count = fields.Integer(
        string='Address Change Requests',
        compute='_compute_record_counts',
        store=False,
    )
    appointment_secretary_count = fields.Integer(
        string='Appointment Secretary Requests',
        compute='_compute_record_counts',
        store=False,
    )
    resignation_secretary_count = fields.Integer(
        string='Resignation Secretary Requests',
        compute='_compute_record_counts',
        store=False,
    )

    @api.depends()
    def _compute_record_counts(self):
        for rec in self:
            rec.address_change_count = self.env['corporate.address.change'].search_count([])
            rec.appointment_secretary_count = self.env['corporate.appointment.secretary'].search_count([])
            rec.resignation_secretary_count = self.env['corporate.resignation.secretary'].search_count([])

    def action_open_address_change(self):
        action = self.env.ref('metro_corporate_docs.corporate_address_change_action').read()[0]
        action.update({'target': 'current'})
        return action

    def action_open_appointment_secretary(self):
        action = self.env.ref('metro_corporate_docs.corporate_appointment_secretary_action').read()[0]
        action.update({'target': 'current'})
        return action

    def action_open_resignation_secretary(self):
        action = self.env.ref('metro_corporate_docs.corporate_resignation_secretary_action').read()[0]
        action.update({'target': 'current'})
        return action

    @api.model
    def get_dashboard_data(self):
        return {
            'address_change_count': self.env['corporate.address.change'].search_count([]),
            'appointment_secretary_count': self.env['corporate.appointment.secretary'].search_count([]),
            'resignation_secretary_count': self.env['corporate.resignation.secretary'].search_count([]),
        }
