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
            'click .o_dashboard_card_open': '_onOpenCard',
            'click .o_dashboard_link': '_onOpenLink'
        },

        init: function (parent, context) {
            this._super.apply(this, arguments);
            this.dashboard_data = {};
        },

        start: function () {
            return this._loadData().then(this._super.bind(this));
        },

        _loadData: function () {
            var self = this;
            return rpc.query({
                model: 'metro.corporate.docs.dashboard',
                method: 'get_dashboard_data',
                args: []
            }).then(function (result) {
                self.dashboard_data = result;
                self.renderElement();
            });
        },

        renderElement: function () {
            this.$el.html(qweb.render('MetroCorporateDocsDashboard', {
                dashboard_data: this.dashboard_data,
            }));
        },

        _onOpenCard: function (event) {
            var target = $(event.currentTarget).data('action');
            this.do_action(target);
        },

        _onOpenLink: function (event) {
            var target = $(event.currentTarget).data('action');
            this.do_action(target);
        }
    });

    core.action_registry.add('metro_corporate_docs.dashboard', MetroCorporateDocsDashboard);
});