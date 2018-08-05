"use strict";
/**
 * Defines the view-model for filters.
 */
define(["knockout", "jquery", "text!runs/filters.html", "runs/filters/queryFilter", "runs/filters/queryFilters"],
    function (ko, $, htmlTemplate, QueryFilter, QueryFilters) {

        /**
         * Experiment Run Filter view-model module.
         *
         * @exports runs/filters
         * @type {{QueryFilter: QueryFilter, QueryFilters: QueryFilters, initialize: initialize}}
         */
        var filters = {
            "QueryFilter": QueryFilter,
            "QueryFilters": QueryFilters,
            /**
             Register <query-filter> HTML tag to display the filter form.

             Displays an inline form to add a new filter to the QueryFilters provided
             as the 'value' parameter. The applied filters are shown in a row
             below the form. The form itself cannot create or display
             other than terminal clause filters on the top level of the QueryFilters.
             (Nested QueryFilters are ignored).
             Example:
             <query-filter params="value: queryFilters"></query-filter>.

             @function
             */
            "initialize": function () {
                ko.components.register("query-filter", {
                    viewModel: function (params) {
                        this.queryFilters = params.value;
                        this.filterToAdd = ko.observable(new QueryFilter("", "", ""));
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

            }

        };
        return filters;
    });
