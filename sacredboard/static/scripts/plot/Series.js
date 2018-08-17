/**
 * @module
 */
define([], function () {
    "use strict";
    /**
     * The Series class is used to store numerical series.
     *
     * Its x-axis can be either a date or a number.
     * The class is consumed by the {@link module:plot/component} module for plotting the data graphically.
     * Issue: [#55](https://github.com/chovanecm/sacredboard/issues/55)
     */
    class Series {
        /**
         * Create a new Series object.
         *
         * @param {ko.observable.Array.<Date>|ko.observable.Array.<number>} x - X data of the series.
         * Either an array of dates or numbers.
         * @param {ko.observable.Array.<number>} y - Y data of the series.
         * @param {string} label - Label of the series.
         *
         * @example new Series(
         * ko.observable([1,2,3]), // x
         * ko.observable([10, 20, 30]), // y
         * ko.observable("x*10")) // label
         *
         * @example new Series(
         * ko.observable([new Date(),new Date(),new Date()]), // x
         * ko.observable([10, 20, 30]), // y
         * ko.observable("x*10")) // label
         */
        constructor(x, y, label) {
            /**
             * X data of the series.
             * @type {ko.observable.Array.<Date>|ko.observable.Array.<Number>}
             */
            this.x = x;
            /**
             * Y data of the series.
             * @type {ko.observable.Array.<Number>}
             */
            this.y = y;
            /**
             * Label of the series.
             * @type {string}
             */
            this.label = label;
        }
    }
    return Series;
});