define("runs/viewModel", ["knockout", "runs/filters", "jquery"], function (ko, filters, $) {
    //Additionaly requires runTable
    var QueryFilters = filters.QueryFilters;
    var QueryFilter = filters.QueryFilter;
    ko.options.deferUpdates = true;
    var viewModel = {
        queryFilters: ko.observable(new QueryFilters()),
        predefinedFilters: {
            "run-alive": new QueryFilter("status", "==", "\"RUNNING\""),
            "run-completed": new QueryFilter("status", "==", "\"COMPLETED\""),
            "run-queued": new QueryFilter("status", "==", "\"QUEUED\""),
            "run-failed": new QueryFilter("status", "==", "\"FAILED\""),
            "run-interrupted": new QueryFilter("status", "==", "\"INTERRUPTED\""),
            "run-dead": new QueryFilter("status", "==", "\"DEAD\"")
        },
        statusFilters: new QueryFilters("or"),

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
    for (var key in viewModel.predefinedFilters) {
        viewModel.statusFilters.addFilter(viewModel.predefinedFilters[key]);
    }
    viewModel.queryFilters().addFilter(viewModel.statusFilters);
    return viewModel;
});
