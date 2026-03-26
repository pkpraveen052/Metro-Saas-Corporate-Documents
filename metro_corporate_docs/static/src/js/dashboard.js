odoo.define('metro_corporate_docs.dashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var session = require('web.session');

    var qweb = core.qweb;

    var MetroCorporateDocsDashboard = AbstractAction.extend({
        template: 'MetroCorporateDocsDashboard',

        events: {
            'click .o_dashboard_open_action': '_onOpenAction',
            'click .o_dashboard_create_action': '_onCreateAction',
            'click .o_dashboard_open_settings': '_onOpenSettings'
        },

        init: function () {
            this._super.apply(this, arguments);
            this.dashboard_data = {};
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._loadData();
            });
        },

        _loadData: function () {
            var self = this;
            return rpc.query({
                model: 'metro.corporate.docs.dashboard',
                method: 'get_dashboard_data',
                args: []
            }).then(function (result) {
                self.dashboard_data = result || {};
                self._renderDashboard();
            });
        },

        _renderDashboard: function () {
            if (!this.$el) {
                return;
            }
            this.$el.html(qweb.render('MetroCorporateDocsDashboard', {
                dashboard_data: this.dashboard_data,
            }));
        },

        _onOpenAction: function (event) {
            var target = $(event.currentTarget).data('action');
            this.do_action(target);
        },

        _onCreateAction: function (event) {
            var model = $(event.currentTarget).data('model');
            if (!model) {
                return;
            }

            var context = this._getDefaultContext();

            this.do_action({
                type: 'ir.actions.act_window',
                res_model: model,
                name: 'Create',
                views: [[false, 'form']],
                target: 'current',
                context: context,
            });
        },

        _onOpenSettings: function (event) {
            var self = this;
            var model = $(event.currentTarget).data('model');
            if (!model) {
                return;
            }

            var context = this._getDefaultContext();

            return rpc.query({
                model: model,
                method: 'search_read',
                args: [[], ['id']],
                kwargs: {limit: 1, order: 'id desc'},
            }).then(function (records) {
                var action = {
                    type: 'ir.actions.act_window',
                    res_model: model,
                    name: 'Settings',
                    views: [[false, 'form']],
                    target: 'current',
                    context: context,
                };
                if (records && records.length) {
                    action.res_id = records[0].id;
                }
                self.do_action(action);
            });
        },

        _getDefaultContext: function () {
            var companyId = session.user_context
                && session.user_context.allowed_company_ids
                && session.user_context.allowed_company_ids[0];
            return companyId ? {default_company_id: companyId} : {};
        },
    });

    core.action_registry.add('metro_corporate_docs.dashboard', MetroCorporateDocsDashboard);
});
