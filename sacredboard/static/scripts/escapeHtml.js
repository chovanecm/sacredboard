"use strict";
define([], function () {
    var entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;",
        "/": "&#x2F;",
        "`": "&#x60;",
        "=": "&#x3D;"
    };

    /**
     * Find and replace HTML-invalid characters in a string.
     *
     * @param {string} string -  The string to be searched.
     * @returns {string} HTML-safe string.
     * @exports escapeHtml
     */
    function replace(string) {
        return String(string).replace(/[&<>"'`=\/]/g, function (s) {
            return entityMap[s]
        });
    }
    return replace;
})
;
