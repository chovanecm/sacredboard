"use strict";
/**
 * A module that defines interface for plotting charts.
 *
 * @module
 */
define([], function () {
    /**
     * A generic plot class to plot a chart.
     *
     * @alias module:plot/plot
     * @constructor
     */
    class Plot {
        /**
         * Define a new plot.
         *
         * @param {DOMObject} element - The DOM element to plot the chart to.
         */
        constructor(element) {
            this._element = element;
            this._xLabel = "";
            this._yLabel = "";
            this._xType = "linear";
            this._yType = "linear";
        }


        /**
         * Do the actual plot.
         */
        plot() {/* abstract */
        }

        /**
         * Add a new data series.
         *
         * @param {Number[]|Date[]]} x - A series of numbers or dates to be plotted against the x axis.
         * @param {Number[]|Date[]]} y - A series of numbers or dates to be plotted against the y axis.
         * @param {string} label - Label of the data series. Must be unique within the chart.
         * @throws TraceAlreadyPresentException - An exception is thrown if the trace with the same label is already present.
         */
        addTrace(x, y, label) {/* abstract */
        }

        /**
         * Remove the data series with a given label.
         *
         * If such series is not known, it might trown an exception.
         *
         * @param {string} label - Label of the data series.
         * @throws TraceNotFoundException - An exception is thrown if the trace with the label has not been found in the chart.
         */
        removeTrace(label) {/* abstract */
        }

        /**
         * @returns {string} The x axis label.
         */
        get xLabel() {
            return this._xLabel;
        }

        /**
         * @returns {string} The y axis label.
         */
        get yLabel() {
            return this._yLabel;
        }

        /**
         * @returns {string} The x axis type (linear/log/date).
         */
        get xType() {
            return this._xType;
        }

        /**
         * @returns {string} The y axis type (linear/log/date).
         */
        get yType() {
            return this._yType;
        }

        set xLabel(xLabel) {
            this._xLabel = xLabel;
        }

        set yLabel(yLabel) {
            this._yLabel = yLabel;
        }

        set xType(xType) {
            this._xType = xType;
        }

        set yType(yType) {
            this._yType = yType;
        }

    }

    Plot.TraceNotFoundException = class extends Error {
        constructor(label) {
            super("Trace '" + label + "' not found in the plot.");
        }
    };

    Plot.TraceAlreadyPresentException = class extends Error {
        constructor(label) {
            super("Trace '" + label + "' is already present in the chart.");
        }
    };

    return Plot;

});



