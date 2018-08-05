define(["knockout"], function (ko) {
    /**
     * Holds objects for displaying them
     * in the dictionary-browser component.
     *
     * The DictEntries are intended to be built as trees:
     * There is one root DictEntry with arbitrary name holding the entire
     * dictionary or array. Its display value is calculated based on the
     * actual value type (array, object, native type).
     *
     * @param {string} name - The display name of this entry.
     * @param {*} value - The value of the entry (object, array, String, Number, Date, null).
     * @class
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
    /**
     * Check whether the value of the DictEntry is a complex type.
     *
     * @returns {boolean} True for objects and arrays, false otherwise.
     */
    DictEntry.prototype.hasChildren = function () {
        return typeof this.value === "object" && this.value !== null;
    };
    /**
     * Generate an array of DictEntries of nested objects.
     *
     * @example <caption>Array.</caption>
     * DictEntry("me", ["hello", "world"]).getChildren()
     * // returns
     * [DictEntry("0", "hello"), DictEntry("1", "world")]
     *
     * @example <caption>Object.</caption>
     * DictEntry("me", {"key1": "value1", "key2": ["hello", "world"]}).getChildren()
     * // returns
     * [DictEntry("key1", "value1"), DictEntry("key2", ["hello", "world"])]
     *
     * @example <caption>Native type.</caption>.
     * DictEntry("me", "string").getChildren()
     * // returns []
     *
     *
     * @returns {DictEntry[]} Array of DictEntries or an empty array for native value types sorted by their keys.
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
    /**
     * Get the keys of the underlying value object and optionally, sort them.
     *
     * In case of arrays, the returned keys are its indices as strings.
     *
     * @param {boolean} sort - Sort the returned array of keys.
     * @returns {string[]} The array of the value keys or an empty array for native types.
     */
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

    /**
     * Get the display name of the DictEntry.
     *
     * @returns {string} Display name.
     */
    DictEntry.prototype.getDisplayName = function () {
        return this.name;
    };

    /**
     * Return the display value for in-line view.
     *
     * @example <caption>Native value.</caption>
     * DictEntry("hello", "world").getDisplayValue()
     * // returns "world"
     *
     * @example <caption>Object.</caption>
     * DictEntry("hello", {"key": "value"}).getDisplayValue()
     * // returns "{...}"
     *
     * @example <caption>Array.</caption>
     * DictEntry("hello", [1,2,3]).getDisplayValue()
     * // returns "[1, 2, 3]"
     *
     * @returns {string} String representation of the value.
     */
    DictEntry.prototype.getDisplayValue = function () {
        return asString(this.value);
    };

    /**
     * Format object to a displayable String.
     *
     * @param {*} value - The value to be converted to a String.
     * @returns {string} String representation of the value.
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
    return DictEntry;
})
;