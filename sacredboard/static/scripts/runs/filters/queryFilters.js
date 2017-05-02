"use strict";
define(["knockout", "jquery"],
    function (ko, $) {
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
         * @exports QueryFilters
         * @constructor
         */
        function QueryFilters(type, filters) {
            var self = this;
            this.filters = ko.observableArray(filters == undefined ? [] : filters);
            this.filters.extend({notify: "always"});
            this.operators = ["==", "!=", "<", "<=", ">", ">=", "regex"];
            this.type = ko.observable(type == undefined ? "and" : type);
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
                            return filter.toDto();
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

        return QueryFilters;
    });