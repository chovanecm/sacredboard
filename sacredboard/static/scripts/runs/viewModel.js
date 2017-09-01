"use strict";
/**
 * The view model for the list of runs.
 *
 * @module runs/viewModel
 */
define(["knockout", "runs/filters/queryFilters", "runs/filters/queryFilter", "runs/filters", "runs/runTable"],
    function (ko, QueryFilters, QueryFilter, filters, runTable) {
        //Additionaly requires runTable
        ko.options.deferUpdates = true;
        filters.initialize();

        /**
         * Define the main view Model for the run list view.
         *
         * Currently manages the run filters only.
         * @exports runs/viewModel
         */
        var viewModel = {
            /**
             * The list of filters applied.
             * The concept currently used allows defining users their custom queries
             * using the <query-filter> HTML component (defined in {@link runs/filters})
             * that are joined together by "AND" (all filters entered must apply at once.
             * Additionally, there is a row of experiment statues (RUNNING, COMPLETED, ...)
             * joined by the "OR" connective that is stored
             * in the {@link viewModel.statusFilters} property.
             * the statusFilters clause and the user-defined filters are joined by AND.
             */
            queryFilters: ko.observable(new QueryFilters()),
            /**
             * Aliases for commonly used filters.
             */
            predefinedFilters: {
                "run-alive": new QueryFilter("status", "==", "\"RUNNING\""),
                "run-completed": new QueryFilter("status", "==", "\"COMPLETED\""),
                "run-queued": new QueryFilter("status", "==", "\"QUEUED\""),
                "run-failed": new QueryFilter("status", "==", "\"FAILED\""),
                "run-interrupted": new QueryFilter("status", "==", "\"INTERRUPTED\""),
                "run-dead": new QueryFilter("status", "==", "\"DEAD\""),
                "run-timeout": new QueryFilter("status", "==", "\"TIMEOUT\"")
            },
            /**
             * Currently applied status filters.
             */
            statusFilters: new QueryFilters("or"),

            /**
             * Transform the curent filters to their Data Transfer Object.
             *
             * @returns {QueryFilterDto} The object to be passed to the Sacredboard Web API.
             */
            getQueryFilterDto: function () {
                return this.queryFilters().toDto();
            },
            /**
             * @callback listenerCallback
             */
            /**
             * Subscribe to changes in the list of applied filters.
             *
             * @param {listenerCallback} listener - The listener function.
             */
            subscribe: function (listener) {
                this.queryFilters().filters.subscribe(listener);
            },

            /**
             * Reload the whole table from the backend.
             */
            reloadTable: function () {
                runTable.reload();
            },

            /**
             * Bind the view model to the view.
             * Should be called after {@link module:runs/viewModel.initialize}.
             */
            bind: function () {
                ko.applyBindings(this);
            },

            /**
             * Initialize the view model and the table of runs.
             *
             * Do not forget to call {@link bind} after that.
             *
             * @param {DOMNode|string} runTableSelector - The HTML <table> element or its selector (e.g. '#run-table')
             * for the list of runs.
             */
            initialize: function (runTableSelector) {
                /* By default, runs any state are displayed.
                 Add them to the statusFilters.q
                 */
                for (var key in this.predefinedFilters) {
                    this.statusFilters.addFilter(this.predefinedFilters[key]);
                }
                // Apply the statusFilters to the view filter.
                this.queryFilters().addFilter(this.statusFilters);


                runTable.initTable(runTableSelector);

                /*
                 * Attach a listener to the viewModel to update the query of
                 * runTable and reload.
                 */
                this.subscribe(function () {
                    runTable.queryFilter = viewModel.getQueryFilterDto();
                    runTable.reload();
                });
            }
        };
        return viewModel;
    });
