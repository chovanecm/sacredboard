define([], function () {
    "use strict";

    /**
     * Format date to the format required by Plot.ly (datapoint).
     *
     * @param {Date} date - The date to be formatted.
     * @returns {string} - A string in format YYYY-MM-DD HH:mm:ss.miliseconds in the local timezone.
     */
    function formatDate(date) {
        var localDate = new Date(date.getTime() -
            date.getTimezoneOffset() * 60 * 1000);
        return localDate.toISOString().replace(/[TZ]/g, " ").trim();
    }
    return formatDate;
});