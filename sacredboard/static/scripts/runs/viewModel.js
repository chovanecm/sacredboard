define(["knockout", "runs/filters", "jquery", "runs/runTable"], function (ko, filters, $, runTable) {
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
        statusFilters: new QueryFilters("or")
    };
    for (var key in viewModel.predefinedFilters) {
        viewModel.statusFilters.addFilter(viewModel.predefinedFilters[key]);
    }

    viewModel.queryFilters().addFilter(viewModel.statusFilters);
    $(document).ready(function () {
        var table = runTable($("#runs"),
            function (config) {
                config.ajax.data = function (request) {
                    request.queryFilter = JSON.stringify(viewModel.queryFilters().toDto());
                };
            }
        );
        viewModel.queryFilters().filters.subscribe(function () {
            table.ajax.reload();
        });

        ko.applyBindings(viewModel);
    });
    return viewModel;
});
