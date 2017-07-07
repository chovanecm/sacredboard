"use strict";

/**
 * The Plot component (`<plot-chart>`) displays a chart of one or more numerical series.
 * This particular module is responsible for definition of the new HTML element.
 * Issue: [#55](https://github.com/chovanecm/sacredboard/issues/55)
 *
 * It can:
 * - plot several series at once
 * - define labels for x and y axes.
 * - show the series' label.
 * - dynamically add/remove series.
 * - axes: numerical and date values.
 *   - Date should be displayed in the local timezone.
 * - switch linear/log scale.
 *
 * ### Usage:
 * ```html
 * <plot-chart params="
 *    series: ko.observableArray([series1, series2, series3]),
 *    xLabel: ko.observable('x label'),
 *    yLabel: ko.observable('y label'),
 *    xType: ko.observable('date'),
 *    yType: ko.observable('linear')"></plot-chart>
 * ```
 * **The values must be Knockout observables.**
 * - `xType` and `yType` are one of `linear`, `log`, `date`. The corresponding axis
 * adjusts accordingly.
 * - Each of the `series` objects is an instance of the {@link Series} class.
 *   - When a property of the {@link Series} changes, the plot should redraw automatically *(note: this is an expensive operation)*.
 *
 * @module plot/component
 */

define(["knockout", "escapeHtml", "text!plot/template.html", "./plotlyplot/PlotlyPlot"],
    /**
     * The chart (plot) component.
     *
     * @param {Knockout} ko - KnockoutJS.
     * @param {escapeHtml} escapeHtml - EscapeHTML function.
     * @param {HTML} htmlTemplate - HTML template of the component.
     * @param {module:plot/plot} Plot - Implementation of the chart plotter.
     */
    function (ko, escapeHtml, htmlTemplate, Plot) {
        ko.components.register("plot-chart", {
            /**
             * View model of the plot component.
             *
             * @param {{series,xLabel,yLabel,xType,yType}} params - Parameters passed to the `<plot-chart params="...">` element.
             * @param {ko.observableArray.Array<Series>} params.series - Array of Series to be plotted.
             * @param {ko.observable.string} params.xLabel - Arbitrary label of the x axis.
             * @param {ko.observable.string} params.yLabel - Arbitrary label of the y axis.
             * @param {ko.observable.string} params.xType - Type of the x axis (linear/log/date).
             * The {@link Series} object expects {@link Date} objects as x-values if `xType` is `"date"`.
             * @param {ko.observable.string} params.yType - Type of the y axis (linear/log/date).
             */
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


        /**
         * Add a new trace to the plot.
         *
         * Also handles changes in underlying data (x, y) and replots them.
         *
         * @param {Plot} plot - Plot to use.
         * @param {Series} aSeries - Series to plot.
         */
        function addTrace(plot, aSeries) {
            function replot() {
                plot.removeTrace(aSeries.label());
                plot.addTrace(aSeries.x(), aSeries.y(), aSeries.label());
            }

            aSeries.x.subscribe(replot);
            aSeries.y.subscribe(replot);
            aSeries.label.subscribe(replot);
            plot.addTrace(aSeries.x(), aSeries.y(), aSeries.label());
        }

        /**
         * Tell Knockout to run the following code on elements with `data-bind="plot: null" attribute`.
         *
         * This will initialize the plotter on a particular HTML element.
         * @type {{init: init, update: update}}
         */
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
                    addTrace(plot, aSeries);
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
                                addTrace(plot, aSeries);
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