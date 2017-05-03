"use strict";
define(["knockout", "runs/filters/queryFilters", "runs/filters/queryFilter", "runs/filters", "runs/runTable"],
    /**
     *
     * @param ko
     * @param QueryFilters
     * @param QueryFilter
     * @param filters
     * @returns {{queryFilters: *, predefinedFilters: {run-alive: *, run-completed: *, run-queued: *, run-failed: *, run-interrupted: *, run-dead: *}, statusFilters: *, getQueryFilterDto: module:runs/viewModel.getQueryFilterDto, subscribe: module:runs/viewModel.subscribe, bind: module:runs/viewModel.bind}}
     */
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
                "run-dead": new QueryFilter("status", "==", "\"DEAD\"")
            },
            /**
             * Currently applied status filters.
             */
            statusFilters: new QueryFilters("or"),

            /**
             * Transform the curent filters to their Data Transfer Object.
             * @returns {QueryFilterDto}
             */
            getQueryFilterDto: function () {
                return this.queryFilters().toDto();
            },
            subscribe: function (listener) {
                this.queryFilters().filters.subscribe(listener);
            },

            reloadTable: function () {
                runTable.reload();
            },

            bind: function () {
                ko.applyBindings(this);
            },

            initialize: function (runTableSelector) {
                /* By default, runs any state are displayed.
                 Add them to the statusFilters.
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
