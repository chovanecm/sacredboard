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
define(["knockout", "text!./template.html", "plot/component"],
    function (ko, htmlTemplate, plotter) {

        /**
         * Metric object.
         *
         * name - property holding the name of the metric
         * timestamps - property holding timestamps of the points (JS Date)
         * steps - property holding step numbers
         * values - property holding values
         * @typedef {{name, timestamps, steps, values}} Metric
         */
        ko.components.register("metrics-plot", {
            /**
             * ViewModel of the metrics-plot component.
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
                //this.axisTypes = ["linear", "log", "date"];
                this.xType = ko.observable("linear");
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
                    var aSeries = {label: metric.name, y: metric.values};
                    if (self.seriesType() == "timestamp") {
                        aSeries["x"] = metric.timestamps;
                    } else {
                        aSeries["x"] = metric.steps;
                    }
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

                this.seriesType.subscribe(
                    /**
                     * Change series type.
                     *
                     * When a change of the x-axis occurs, remove current series
                     * from the plot and replace them with the same series but
                     * with an appropriaate x-axis data (date/number).
                     *
                     * @param {string} newValue - New x axis type (step/timestamp).
                     */
                    function (newValue) {
                        self.series.removeAll();

                        self.selectedMetrics().forEach(function (metric) {
                            self.series.push(self.convertToSeries(metric));
                        });
                    }, this);
            },
            template: htmlTemplate
        });
    });