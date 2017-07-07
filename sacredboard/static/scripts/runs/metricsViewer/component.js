"use strict";
/**
 * Metrics-viewer component.
 *
 * The purpose of the component is to handle the logic of of extraction metrics
 * data from the run and from the backend and to pass data to the metrics-plot component.
 *
 * Issue: https://github.com/chovanecm/sacredboard/issues/59
 * @module
 */
define(["knockout", "text!./template.html", "./ProxiedMetric", "metricsPlot/component"],
    function (ko, htmlTemplate, ProxiedMetric, metricsPlot) {
        ko.components.register("metrics-viewer", {
            viewModel: function (params) {
                var self = this;
                this.run = params.run;
                this.metrics = ko.observableArray();

                this.onMetricFetch = function (metric) {
                    self.selectedMetrics.remove(metric);
                    self.selectedMetrics.push(metric);
                };

                // initialize the metrics
                if (this.run.hasOwnProperty("info")) {
                    var info = this.run.info;
                    if (info.hasOwnProperty("metrics")) {
                        info.metrics.forEach(function (aMetric) {
                            self.metrics.push(new ProxiedMetric(
                                ko.observable(aMetric["name"]),
                                self.run._id,
                                aMetric["id"]
                            ));
                        });
                    }
                }
            },
            template: htmlTemplate
        });
    });