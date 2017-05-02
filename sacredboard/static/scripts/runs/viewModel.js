"use strict";
define(["knockout", "runs/filters/queryFilters", "runs/filters/queryFilter", "runs/filters", "jquery"],
    function (ko, QueryFilters, QueryFilter, filters, $) {
    //Additionaly requires runTable
    ko.options.deferUpdates = true;

    /**
     * Define the main view Model for the run list view.
     *
     * Currently manages the run filters only.
     * @exports runs/viewModel
     * @type {{queryFilters: *, predefinedFilters: {run-alive: QueryFilter, run-completed: QueryFilter, run-queued: QueryFilter, run-failed: QueryFilter, run-interrupted: QueryFilter, run-dead: QueryFilter}, statusFilters: QueryFilters, getQueryFilterDto: getQueryFilterDto, subscribe: subscribe, bind: bind}}
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

        bind: function () {
            ko.applyBindings(this);
        }
    };
    /* By default, runs any state are displayed.
       Add them to the statusFilters.
     */
    for (var key in viewModel.predefinedFilters) {
        viewModel.statusFilters.addFilter(viewModel.predefinedFilters[key]);
    }
    // Apply the statusFilters to the view filter.
    viewModel.queryFilters().addFilter(viewModel.statusFilters);
    return viewModel;
});
