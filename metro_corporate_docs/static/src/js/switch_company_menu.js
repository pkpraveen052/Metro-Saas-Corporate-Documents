odoo.define('metro_corporate_docs.pdf_preview', function(require) {
    "use strict";

    var DocumentViewer = require('mail.DocumentViewer');
    var core = require('web.core');

    function KsViewPDF(parent, action) {
        var ks_activeAttachmentID = action.params.attachment_id;

        var ks_attachment = [{
            id: ks_activeAttachmentID,
            mimetype: 'application/pdf',
            name: 'Preview',
            url: "/web/content/" + ks_activeAttachmentID + "?download=false"
        }];

        var viewer = new DocumentViewer(parent, ks_attachment, ks_activeAttachmentID);
        viewer.appendTo($('body'));

        viewer.on('closed', self, function () {
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: action.params.model,
                res_id: action.params.res_id,
                views: [[false, 'form']],
                target: 'current',
            });
        });

    }

    core.action_registry.add("corporate_view_report_pdf", KsViewPDF);
});