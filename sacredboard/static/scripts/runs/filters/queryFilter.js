"use strict";
/**
 * @module runs/filters/queryFilter
 */
define(["knockout", "enquotedStringOrNumberValidator"],
    function (ko, stringOrNumberValidator) {
        /**
         * Terminal clause for filters.
         *
         * A terminal clause is a terminal part of the whole query.
         * It means that it cannot contain subclauses.
         *
         * @example
         * QueryFilter("host.hostname", "!=", "node1")
         *
         * @param {string} field - The database field to be filtered by.
         * @param {string} operator - The operator to be used. {@link QueryFilters.operators).
         * @param {string|number} value - The value to be applied in the filter (a primitive type).
         * @class
         * @alias module:runs/filter/queryFilter
         */
        class QueryFilter {
            constructor(field, operator, value) {
                var self = this;
                /* In accordance with https://github.com/chovanecm/sacredboard/issues/8
             the user searches by default in the config scope.
             He may, however, search everywhere if he prepends "." to the beginning
             of the query, e.g. ".host.hostname"
             */
                this.defaultScope = "config.";
                /**
                 * The actual user input, e.g. "seed" or .host.hostname
                 */
                this.userInputField = ko.observable("");

                /**
                 * The prefix to be prepended to the user input.
                 * Normally "config." or "".
                 * Calculated.
                 */
                this.fieldScope = ko.pureComputed(function () {
                    if (self.userInputField().startsWith(".")) {
                        return "";
                    } else {
                        return self.defaultScope;
                    }
                }, this);
                /**
                 * The actual field name to be filtered by. If user inputs "seed",
                 * this should resolve to "config.seed".
                 * If the user inputs ".host.hostname", this will resolve to
                 * "host.hostname".
                 * Vice versa, if the property is set to "host.hostname", it will
                 * set the user input property to ".host.hostname" so that the view updates
                 * accordingly to what the user expects.
                 *
                 * Computed read/write.
                 */
                this.field = ko.pureComputed({
                    read: function () {
                        if (self.userInputField().startsWith(".")) {
                            return self.userInputField().substring(1);
                        } else if (self.userInputField() != "") {
                            return self.fieldScope() + self.userInputField();
                        } else {
                            return "";
                        }
                    },
                    write: function (value) {
                        if (value.startsWith(self.defaultScope)) {
                            // Set the user input field without the default scope name
                            self.userInputField(value.substring(self.defaultScope.length));
                        } else if (value != "") {
                            self.userInputField("." + value);
                        } else {
                            self.userInputField("");
                        }
                    }
                });
                // Set the initial field value
                this.field(field);

                /**
                 * Operator of the filter ("==", "<", etc.)
                 */
                this.operator = ko.observable(operator);
                /**
                 * The filter value that the user inputs.
                 * The input should be either enquoted String ("string") or a number
                 * without quotes (123.456).
                 *
                 * The format of the entered value is immediately checked by the
                 * validateJSONValue validator from the enquotedStringOrNumberValidator
                 * module (required by this module)
                 */
                this.value = ko.observable(value).extend(
                    {
                        validateJSONValue: this
                    });

                /**
                 * JavaScript native value of the user's value input.
                 *
                 * The value that user inputs to {@link value} is a string.
                 * A number (input without quotes) must be converted to a number in JS
                 * and an enquoted "string" must be trimmed from the extra quotes.
                 */
                this.nativeValue = ko.pureComputed(function () {
                    return this.holdsDateValue() ? this.getStrDateValue() : JSON.parse(this.value());
                }, this);
            }

            holdsDateValue() {
                return this.value().startsWith("d:");
            }

            getStrDateValue() {
                if (!this.holdsDateValue()) {
                    throw new Error("Cannot get string date value of a non-date query value: " + this.value());
                }
                return this.value().substr(2);
            }

            /**
             * Return a copy of the object.
             *
             * @returns {QueryFilter} A copy of the current object.
             */
            clone() {
                return new QueryFilter(this.field(), this.operator(), this.value());
            }

            /**
             * A serialiable Data Transfer Object of a QueryFilter.
             *
             * @typedef {{field: String, operator: String, value: primitive}} QueryFilterDto
             */
            /**
             * Convert QueryFilter to its Data Transfer Object.
             *
             * @returns {QueryFilterDto} A simple object representing
             * the filter for serialisation as requested by the Sacredboard API.
             */
            toDto() {
                const dto = {
                    "field": this.field(),
                    "operator": this.operator(),
                    "value": this.nativeValue()
                };
                if (this.holdsDateValue()) {
                    dto["valueType"] = "DateTime";
                }
                return dto;
            }

            addParentObserver(observer) {
                /* Do nothing, we consider a QueryFilter to be used as immutable object */
            }
        }

        return QueryFilter;
    }
);
