"use strict";
/**
 * Component for displaying the detail view of a run.
 *
 * Issue [#65](https://github.com/chovanecm/sacredboard/issues/65)
 *
 * @module
 */
define(
    [
        "knockout",
        "escapeHtml",
        "text!./template.html",
        "runs/dictionaryBrowser/component",
        "runs/metricsViewer/component",
        "jquery"],
    function (ko, escapeHtml, htmlTemplate, dictionaryBrowser, metricsViewer, $) {
        ko.components.register("detail-view", {
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.run = params.run;
                this.tensorflowDirs = this.run.object.info.tensorflow || {logdirs: []};

                /**
                 * Delete run with given ID.
                 *
                 * Hopefully only a temporary solution. (Should have its own module if not a class).
                 *
                 * Issue: [#64](https://github.com/chovanecm/sacredboard/issues/64).
                 */
                this.deleteRun = function () {
                    if (!confirm("Are you sure to delete run id " + self.run.id + "?")) {
                        return;
                    }
                    $.ajax({
                        method: "DELETE",
                        url: "/api/run/" + self.run.id
                    }).done(function (msg) {
                        alert("Data Saved: " + msg);
                    });
                };
            },
            template: htmlTemplate
        });


    });