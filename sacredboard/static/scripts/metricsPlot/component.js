"use strict";
/**
 * Metric Plot component.
 *
 * Given a list of available metrics, this component controls the plot element
 * to add and remove series.
 *
 * Issue: https://github.com/chovanecm/sacredboard/issues/59
 * @module
 */
define(["knockout", "text!./template.html", "plot/component", "runs/Metric"],
    function (ko, htmlTemplate, plotter /* plotter for <plot-chart> HTML element */, Metric) {

        ko.components.register("metrics-plot", {
            /**
             * ViewModel of the metrics-plot component.
             *
             * It holds all the metrics available, the metrics selected by
             * the user to be plotted and calculates the actual series
             * for the plot-chart component.
             *
             * @param {{availableMetrics}} params - Parameters of the viewModel.
             * @param {Metric[]} params.availableMetrics - Knockout observable array of {@link Metric}.
             * @class
             */
            viewModel: function (params) {
                var self = this;
                /**
                 * Metrics available.
                 *
                 * Array of {@link Metric} objects.
                 * @type ko.observableArray
                 * @memberOf viewModel
                 */
                this.availableMetrics = params.availableMetrics;
                /**
                 * Metrics selected to be plotted.
                 *
                 * @memberOf viewModel
                 */
                this.selectedMetrics = ko.observableArray();

                this.selectAllMetrics = ko.pureComputed({
                    read: function () {
                        return self.availableMetrics().length === self.selectedMetrics().length;
                    },
                    write: function (value) {
                        if (value == true) {
                            self.availableMetrics()
                                .filter(metric => self.selectedMetrics.indexOf(metric) < 0)
                                .forEach(metric => self.selectedMetrics.push(metric));
                        } else {
                            self.selectedMetrics.removeAll();
                        }
                    }
                });

                //this.axisTypes = ["linear", "log", "date"];.
                /**
                 * One of linear, log, date
                 */
                this.xType = ko.observable("linear");
                /**
                 * One of linear, log, date
                 */
                this.yType = ko.observable("linear");
                this.yLabel = ko.observable("value");
                /**
                 * Decide the x-axis label based on x-axis type.
                 *
                 * @memberOf viewModel
                 */
                this.xLabel = ko.pureComputed(function () {
                    if (self.xType() == "date") {
                        return "time";
                    } else {
                        return "step";
                    }
                });
                /**
                 * Series data for the plot component.
                 *
                 * The content depends on the metrics selected and the type of the
                 * x axis. (date/number)
                 *
                 * @memberOf viewModel
                 */
                this.series = ko.observableArray();
                this.seriesType = ko.pureComputed(function () {
                    return self.xType() == "date" ? "timestamp" : "step";
                });

                /**
                 * Converts a metric object to a Series object.
                 *
                 * @param {Metric} metric - Metric object.
                 * @returns {{label, x, y}} - Series object as required by the Plot component.
                 * @function convertToSeries
                 */
                this.convertToSeries = function (metric) {
                    var aSeries = {
                        label: metric.name,
                        y: metric.values,
                        x: ko.pureComputed(function () {
                            if (self.seriesType() == "timestamp") {
                                return metric.timestamps();
                            } else {
                                return metric.steps();
                            }
                        })
                    };
                    return aSeries;
                };


                this.selectedMetrics.subscribe(
                    /**
                     * Update the series array accordingly when an element is added or removed from selection.
                     *
                     * @param {Array} changes - Changes to the selectedMetrics array.
                     */
                    function (changes) {
                        changes.forEach(function (change) {
                            var value = change["value"];
                            var status = change["status"];
                            var index = change["index"];
                            if (status == "added") {
                                self.series.push(self.convertToSeries(value));
                            } else if (status == "deleted") {
                                self.series.remove(function (item) {
                                    return item.label() == value.name();
                                });
                            }
                        });
                    }, null, "arrayChange");
            },
            template: htmlTemplate
        });
    });