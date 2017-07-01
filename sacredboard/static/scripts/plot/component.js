"use strict";

/**
 * The Plot component displays a chart of one or more numerical series.
 *
 * Issue: https://github.com/chovanecm/sacredboard/issues/55
 *
 * It can:
 * - plot several series at once
 * - define labels for x and y labels
 * - show the series' label
 * - dynamically add/remove series.
 * - The x-axis must support both numerical and date values. (TODO)
 * Usage: see the issue or test.html for example.
 */


/**
 * A numeric series with a label.
 *
 * @typedef {{x: array, y: array, label: string}} Series
 */
define(["knockout", "escapeHtml", "text!plot/template.html", "plotly"],
    function (ko, escapeHtml, htmlTemplate, Plotly) {
        ko.components.register("plot", {
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.seriesArray = params.series;
                this.xLabel = params.xLabel;
                this.yLabel = params.yLabel;
            },
            template: htmlTemplate
        });

        ko.bindingHandlers.plot = {
            init: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                var layout = {
                    showlegend: true
                };
                var data = seriesToTraces(bindingContext.$data.seriesArray(), "scatter");
                Plotly.newPlot(element, data, layout);

                bindingContext.$data.seriesArray.subscribe(
                    /**
                     * When a change is detected in the underlying array of series,
                     * add / remove the corresponding trace to / from the chart accordingly.
                     *
                     * @param {Array} changes - Array of changes emitted by the array.
                     */
                    function (changes) {
                        for (var key in changes) {
                            var change = changes[key];
                            if (change["status"] == "added") {
                                var value = seriesToTraces([change["value"]]);
                                Plotly.addTraces(element, value, change["index"]);
                            } else if (change["status"] == "deleted") {
                                Plotly.deleteTraces(element, change["index"]);
                            }
                        }
                    }, null, "arrayChange");

            },
            update: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                // Set x and y axes label
                var xLabel = bindingContext.$data.xLabel();
                var yLabel = bindingContext.$data.yLabel();
                setAxesLabel(element, xLabel, yLabel);
            }
        };
        /**
         *  Convert an array of series to a trace for Plot.ly.
         *
         * @param {Series[]} array - Array of series to be plotted.
         * @param {string} type - Plot.ly chart type (e.g. scatter).
         */
        function seriesToTraces(array, type) {
            return array.map(function (aSeries) {
                return {
                    x: aSeries.x(),
                    y: aSeries.y(),
                    name: aSeries.label(),
                    showlegend: true,
                    visible: "legendonly",
                    type: type
                };
            });
        }

        /**
         * Generate an object for updating Plot.ly layout based on x and y axis labels.
         *
         * @param {string|null} xLabel - Label of the x axis. Null for keeping as is.
         * @param {string|null} yLabel - Label of the y axis. Null for keeping as is.
         * @returns {{}} A layout update for Plot.ly's <code>relayout()</code> method.
         */
        function createLayoutUpdate(xLabel, yLabel) {
            var layoutUpdate = {};
            if (xLabel != null) {
                layoutUpdate["xaxis.title"] = xLabel;
            }
            if (yLabel != null) {
                layoutUpdate["yaxis.title"] = yLabel;
            }
            return layoutUpdate;
        }

        /**
         * Set labels for the x and y axis.
         *
         * @param {string|null} xLabel - Label of the x axis. Null for keeping as is.
         * @param {string|null} yLabel - Label of the y axis. Null for keeping as is.
         * @param element - A DOM element with the chart to update.
         */
        function setAxesLabel(element, xLabel, yLabel) {
            var layoutUpdate = createLayoutUpdate(xLabel, yLabel);
            Plotly.relayout(element, layoutUpdate);
        }

    });