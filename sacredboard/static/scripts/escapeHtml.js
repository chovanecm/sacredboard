define("escapeHtml", [], function () {
    var entityMap = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;',
        '`': '&#x60;',
        '=': '&#x3D;'
    };

    /**
     * Replaces some characters with their HTML equivalents
     * @param string
     * @return {String}
     * @export escapeHtml
     */
    function replace(string) {
        return String(string).replace(/[&<>"'`=\/]/g, function (s) {
            return entityMap[s];
        })
    }
    return replace;
})
;
