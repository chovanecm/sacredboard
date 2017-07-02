"use strict";



/**
 * A numeric series with a label.
 *
 * @typedef {{x: array, y: array, label: string}} Series
 */
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
 * - axes: numerical and date values.
 *   - Date should be displayed in the local timezone.
 * - switch linear/log scale.
 * Usage: see the issue or test.html for example.
 *
 * @module
 */

define(["knockout", "escapeHtml", "text!plot/template.html", "./plotlyplot/PlotlyPlot"],
    /**
     * The chart (plot) component.
     *
     * @param {Knockout} ko - KnockoutJS.
     * @param {escapeHtml} escapeHtml - EscapeHTML function.
     * @param {HTML} htmlTemplate - HTML template.
     * @param {module:plot/plot} Plot - Implementation of the chart plotter.
     */
    function (ko, escapeHtml, htmlTemplate, Plot) {
        ko.components.register("plot", {
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.seriesArray = params.series;
                this.xLabel = params.xLabel || ko.observable("x");
                this.yLabel = params.yLabel || ko.observable("y");
                this.xType = params.xType || ko.observable("-");
                this.yType = params.yType || ko.observable("-");
                this.plot = null;
            },
            template: htmlTemplate
        });

        ko.bindingHandlers.plot = {

            /**
             * Initialize the chart.
             *
             * @param {DOMElement} element - The DOM element to initialize the chart within.
             * @param {Object} valueAccessor - See knockout doc.
             * @param {Object} allBindings - See knockout doc.
             * @param {Object} viewModel - Deprecated. See knockout doc.
             * @param {Object} bindingContext - The binding context (and a gateway to the view model).
             */
            init: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                // Initialize our plot object
                var plot = bindingContext.$data.plot = new Plot(element);

                // Add each of the series to the chart.
                bindingContext.$data.seriesArray().forEach(function (aSeries) {
                    plot.addTrace(aSeries.x(), aSeries.y(), aSeries.label());
                });
                // Do the actual plot.
                plot.plot();

                bindingContext.$data.seriesArray.subscribe(
                    /**
                     * When a change is detected in the underlying array of series,
                     * add / remove the corresponding trace to / from the chart accordingly.
                     *
                     * @param {Array} changes - Array of changes emitted by the array.
                     */
                    function (changes) {
                        changes.forEach(function (change) {
                            var aSeries;
                            if (change["status"] == "added") {
                                aSeries = change["value"];
                                plot.addTrace(aSeries.x(), aSeries.y(), aSeries.label());
                            } else if (change["status"] == "deleted") {
                                aSeries = change["value"];
                                plot.removeTrace(aSeries.label());
                            }
                        });
                    }, null, "arrayChange");

            },
            /**
             * Update chart.
             *
             * Called automatically when any of the properties in the method
             * body changes.
             *
             * @param {DOMElement} element -  DOM element with Plot.ly chart.
             * @param {Object} valueAccessor - See knockout doc.
             * @param {Object} allBindings - See knockout doc.
             * @param {Object} viewModel - Deprecated. See knockout doc.
             * @param {Object} bindingContext - The binding context (and a gateway to the view model).
             */
            update: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                var plot = bindingContext.$data.plot;
                // Set x and y axes label
                var xLabel = bindingContext.$data.xLabel();
                var yLabel = bindingContext.$data.yLabel();
                plot.xLabel = xLabel;
                plot.yLabel = yLabel;

                var xType = bindingContext.$data.xType();
                var yType = bindingContext.$data.yType();
                plot.xType = xType;
                plot.yType = yType;
            }
        };

    });