define(["knockout"], function (ko) {
    /**
     * Holds objects for displaying them
     * in the dictionary-browser component.
     *
     * The DictEntries are intended to be built as trees:
     * there is one root DictEntry with arbitrary name holding the entire
     * dictionary or array. Its display value is calculated based on the
     * actual value type (array, object, native type).
     *
     * @param {String} name The
     * @param {*} value
     * @constructor
     */
    function DictEntry(name, value) {
        this.name = name;
        this.value = value;
        this.contentCollapsed = ko.observable(true);
    }

    /**
     * Toggle collapse state to display or show nested objects.
     */
    DictEntry.prototype.toggleCollapse = function () {
        if (this.hasChildren()) {
            this.contentCollapsed(!this.contentCollapsed());
        }
    };
    DictEntry.prototype.hasChildren = function () {
        return typeof this.value === "object" && this.value !== null;
    };
    /**
     * Generate DictEntries for its children, sorted by key name.
     * @returns {DictEntry[]}
     */
    DictEntry.prototype.getChildren = function () {
        if (this.hasChildren()) {
            var keys = this.getChildrenKeys(true);
            var arr = [];
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                arr.push(new DictEntry(key, this.value[key]));
            }

            return arr;
        } else {
            return [];
        }
    };
    DictEntry.prototype.getChildrenKeys = function (sort) {
        var keys = [];
        for (var valKey in this.value) {
            keys.push(valKey);
        }
        if (sort && !(this.value instanceof Array)) {
            // Sort only non-array indices (array is indexed from 0 by default).
            keys.sort();
        }
        return keys;
    };

    DictEntry.prototype.getDisplayName = function () {
        return this.name;
    };

    /**
     * Return display value for in-line view
     * @returns {String}
     */
    DictEntry.prototype.getDisplayValue = function () {
        return asString(this.value);
    };

    /**
     * Format object to a displayable String
     * @param value
     * @returns {String}
     */
    function asString(value) {
        if (value instanceof Array) {

            return "[" +
                value.map(function (element) {
                    return asString(element);
                }).join(", ")
                + "]";
        } else if (value instanceof Date) {
            return value.toLocaleString();
        } else if (value === null) {
            return "null";
        } else if (typeof value === "object") {
            return "{...}";
        } else {
            return "" + value;
        }
    }

    DictEntry.prototype.EMPTY = "";
    return DictEntry;
})
;