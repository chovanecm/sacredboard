define(["./formatDate"], function (formatDate) {
    "use strict";
    /**
     * Convert given data points for PlotlyPlot.
     *
     * Return number as is or dates as a formatted string that is accepted by Plotly.
     *
     * @param {Date[]|Number[]} dataPoints - Array of numbers or dates to be used as values.
     */
    function convertDataPoints(dataPoints) {
        return dataPoints.map(function (value) {
            if (value instanceof Date) {
                return formatDate(value);
            } else {
                return value;
            }
        });
    }

    return convertDataPoints;
});