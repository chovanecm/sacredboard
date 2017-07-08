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
            /**
             * Remove run.
             *
             * @callback deleteRunHandler
             */
            /**
             *
             * @param {{run,deleteRunHandler}} params - Parameters of the component.
             * @param {{object, id}} params.run  - The object from the /api/run/<id> resource.
             * @param {deleteRunHandler} params.deleteRunHandler  - The logic to remove the run.
             *
             */
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.run = params.run;
                this._deleteFunction = params.deleteRunHandler ||
                    function (id) {
                        throw "Not Implemented";
                    };
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
                    this._deleteFunction(self.run.id);
                };
            },
            template: htmlTemplate
        });


    });