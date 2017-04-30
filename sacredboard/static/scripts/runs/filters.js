"use strict";
/**
 * Defines the view-model for filters.
 */
define("runs/filters", ["knockout", "jquery", "text!runs/filters.html", "enquotedStringOrNumberValidator"],
    function (ko, $, htmlTemplate, stringOrNumberValidator) {

        /**
         * Terminal clause for filters.
         *
         * A terminal clause is a terminal part of the whole query.
         * It means that it cannot contain subclauses.
         *
         * Example: QueryFilter("host.hostname", "!=", "node1")
         *
         * @param {String} field The database field to be filtered by.
         * @param {String} operator The operator to be used.
         *        {@link QueryFilters.operators)
         * @param value The value to be applied in the filter (a primitive type).
         * @constructor
         */
        function QueryFilter(field, operator, value) {
            var self = this;
            /* In accordance with https://github.com/chovanecm/sacredboard/issues/8
             the user searches by default in the config scope.
             He may, however, search everywhere if he prepends "." to the beginning
             of the query, e.g. ".host.hostname"
             */
            var defaultScope = "config.";
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
                    return defaultScope;
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
                    if (value.startsWith(defaultScope)) {
                        // Set the user input field without the default scope name
                        self.userInputField(value.substring(defaultScope.length));
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
             * module (required by this runs/filters module)
             */
            this.value = ko.observable(value).extend({validateJSONValue: this});
            /**
             * JavaScript native value of the user's value input.
             *
             * The value that user inputs to {@link value} is a string.
             * A number (input without quotes) must be converted to a number in JS
             * and an enquoted "string" must be trimmed from the extra quotes.
             */
            this.nativeValue = ko.pureComputed(function () {
                return JSON.parse(this.value());
            }, this);

            /**
             * Return a copy of the object.
             * @returns {QueryFilter}
             */
            this.clone = function () {
                return new QueryFilter(this.field(), this.operator(), this.value())
            };

            /**
             * A serialiable Data Transfer Object of a QueryFilter.
             * @typedef {{field: String, operator: String, value: primitive}} QueryFilterDto
             */
            /**
             * Convert QueryFilter to its Data Transfer Object
             * @return QueryFilterDto
             */
            this.toDto = function () {
                return {
                    "field": self.field(),
                    "operator": self.operator(),
                    "value": self.nativeValue()
                };
            };

            this.addParentObserver = function (observer) {
                /* Do nothing, we consider a QueryFilter to be used as immutable object */
            };
        }

        /**
         * The QueryFilters object is a set of filters to be applied together.
         *
         * A query like "(A == 1 AND B < 10) OR (X == 'hello')"
         * can be constructed in the following way:
         * <pre><code>
         * new QueryFilters("or", [ new QueryFilter('X', '==', 'hello'),
         *                          new QueryFilters('and', [
         *                              new QueryFilter('A', '==', 1),
         *                              new QueryFilter('B', '<', 10)
         *                                          ])
         *                 ]);
         * </code></pre>
         * @param {String} type either 'and' or 'or'. Default: 'and'
         * @param {Array.(QueryFilter|QueryFilters)} filters
         * @constructor
         */
        function QueryFilters(type, filters) {
            var self = this;

            this.filters = ko.observableArray(filters == undefined ? [] : filters);
            this.filters.extend({notify: 'always'});
            this.operators = ['==', '!=', '<', '<=', '>', '>=', 'regex'];
            this.type = ko.observable(type == undefined ? 'and' : type);
            self.addFilter = function (filter) {
                self.filters.push(filter);
                filter.addParentObserver(self.filters);
            };
            self.removeFilter = function (filter) {
                self.filters.remove(filter);

            };

            /**
             * Data Transfer Object for QueryFilters.
             * @typedef {{type: String, filters: Array.(QueryFilterDto|QueryFiltersDto)}} QueryFiltersDto
             */
            /**
             * Transform QueryFilters to its Data Transfer Object that can be
             * serialized and sent to backend.
             * @return QueryFiltersDto
             */
            self.toDto = function () {
                return {
                    "type": self.type(),
                    "filters": $.map(self.filters(),
                        function (filter) {
                            return filter.toDto()
                        })
                };
            };
            self.addParentObserver = function (observer) {
                //Note: The observer must be set to always notify subscribers even if it doesn't detect a change.
                self.filters.subscribe(function () {
                    observer.notifySubscribers();
                });
            };
        }

        /* Register <query-filter> HTML tag to display the filter form.

         Displays an inline form to add a new filter to the QueryFilters provided
         as the 'value' parameter. The applied filters are shown in a row
         below the form. The form itself cannot create or display
         other than terminal clause filters on the top level of the QueryFilters.
         (Nested QueryFilters are ignored).
         Example:
         <query-filter params="value: queryFilters"></query-filter>
         */
        ko.components.register('query-filter', {
            viewModel: function (params) {
                this.queryFilters = params.value;
                this.filterToAdd = ko.observable(new QueryFilter("", "", "", "string"));
                this.addFilter = function () {
                    if (this.filterReadyToAdd()) {
                        this.queryFilters().addFilter(this.filterToAdd().clone());
                    }
                };

                this.filterReadyToAdd = function () {
                    var fieldAndOperatorSet = (this.filterToAdd().field() != "" && this.filterToAdd().operator() != "");
                    return fieldAndOperatorSet && !this.filterToAdd().value.hasError();
                };

            },
            template: htmlTemplate
        });

        /**
         * Experiment Run Filter view-model module.
         *
         * @exports runs/filters
         * @type {{QueryFilter: QueryFilter, QueryFilters: QueryFilters}}
         */
        var filters = {
            "QueryFilter": QueryFilter,
            "QueryFilters": QueryFilters
        };
        return filters;
    });
