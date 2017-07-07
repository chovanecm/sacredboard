/**
 * Metric class as defined in Issue #59.
 *
 * Issue: https://github.com/chovanecm/sacredboard/issues/59
 *
 * @module
 */

define([], function () {
    "use strict";
    class Metric {
        /**
         * Constructor of the Metric class.
         *
         * @param {string} name - Name of the metric (knockout observable).
         * @param {number[]} steps - Array of steps of measurements (knockout observable).
         * @param {Date[]} timestamps - Array of timestamps of measurements (knockout observable).
         * @param {number[]} values - Array of values of measurements (knockout observable).
         */
        constructor(name, steps, timestamps, values) {
            this.name = name;
            this.timestamps = timestamps;
            this.steps = steps;
            this.values = values;
        }
    }
    return Metric;
});