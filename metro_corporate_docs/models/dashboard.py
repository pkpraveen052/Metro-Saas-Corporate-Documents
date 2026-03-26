# -*- coding: utf-8 -*-
from odoo import api, models


class MetroCorporateDocsDashboard(models.AbstractModel):
    _name = 'metro.corporate.docs.dashboard'
    _description = 'Corporate Documents Dashboard Data Provider'

    @api.model
    def get_dashboard_data(self):
        return {
            'address_change_count': self.env['corporate.address.change'].search_count([]),
            'appointment_secretary_count': self.env['corporate.appointment.secretary'].search_count([]),
            'resignation_secretary_count': self.env['corporate.resignation.secretary'].search_count([]),
        }
