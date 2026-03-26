odoo.define('metro_corporate_docs.dashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var qweb = core.qweb;

    var MetroCorporateDocsDashboard = AbstractAction.extend({
        template: 'MetroCorporateDocsDashboard',

        events: {
            'click .o_dashboard_open_action': '_onOpenAction'
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
            var $button = $(event.currentTarget);
            var model = $button.data('model');
            var name = $button.data('name') || 'Records';

            this.do_action({
                type: 'ir.actions.act_window',
                name: name,
                res_model: model,
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                target: 'current'
            });
        },
    });

    core.action_registry.add('metro_corporate_docs.dashboard', MetroCorporateDocsDashboard);
});
