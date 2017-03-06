/**
 * Created by Martin on 4. 3. 2017.
 */
function QueryFilter(field, operator, value, valueType) {
    this.field = ko.observable(field);
    this.operator = ko.observable(operator);
    this.value = ko.observable(value);
    this.valueType = ko.observable(valueType);

    this.clone = function () {
        return new QueryFilter(this.field(), this.operator(), this.value())
    };

    this.toDto = function () {
        var targetValue = (this.valueType() == "number") ? Number(this.value()) : this.value();
        return {"field": this.field(), "operator": this.operator(), "value": targetValue};
    }
}

function QueryFilters() {
    let self = this;
    this.filters = ko.observableArray([]);
    this.operators = ['==', '!=', '<', '<=', '>', '>=', 'regex'];
    this.valueTypes = ['string', 'number'];

    self.addFilter = function (filter) {
        self.filters.push(filter);
    };
    self.removeFilter = function () {
        self.filters.remove(this);
    }
}

ko.components.register('query-filter', {
    viewModel: function (params) {
        this.queryFilters = params.value;
        this.filterToAdd = ko.observable(new QueryFilter("", "", "", "string"));
        this.addFilter = function () {
            if (this.filterReadyToAdd()) {
                this.queryFilters().addFilter(this.filterToAdd());
                this.filterToAdd(this.filterToAdd().clone());
            }
        };
        this.filterReadyToAdd = function () {
            return (this.filterToAdd().field() != "" && this.filterToAdd().operator() != "");
        };
    },
    template: ` <form class="form-inline" data-bind="submit: addFilter">
                <div class="form-group">
                    <label class="sr-only" for="queryField">Field name</label>
                    <input type="text" class="form-control" id="queryField" placeholder="host.hostname"
                           data-bind='value: filterToAdd().field,  valueUpdate: "afterkeydown"'>
                </div>
                <div class="form-group">
                    <label class="sr-only" for="queryOperator">Operator</label>
                    <select id="queryOperator" class="form-control" data-bind="options: queryFilters().operators,
                                                                           value: filterToAdd().operator"></select>
                </div>
                <div class="form-group">
                    <label class="sr-only" for="queryValue">Query value</label>
                    <input type="text" class="form-control" id="queryValue" placeholder="value" data-bind="value: filterToAdd().value,
                                                                                                       valueUpdate: 'afterkeydown'">
                </div>
                <div class="form-group">
                    <label class="sr-only" for="queryvalueType">Treat as</label>
                    <select id="queryvalueType" class="form-control" data-bind="options: queryFilters().valueTypes,
                                                                           value: filterToAdd().valueType"></select>
                </div>
                <button type="submit" class="btn btn-default" data-bind="enable: filterReadyToAdd()">Add filter</button>
            </form>
            <div class="row-fluid clearfix" style="margin-top: 1eM">
                <div class="col-md-12" data-bind="with: queryFilters">
                    <div data-bind="foreach: filters">
                        <div class="query-filter">
                            <span data-bind="text: field"></span>
                            <span data-bind="text: operator"></span>
                            <span data-bind="visible: valueType() == 'string'">"</span><span data-bind="text: value"></span><span data-bind="visible: valueType() == 'string'">"</span>
                            <a href="#" data-bind="click: $parent.removeFilter">[X]</a>
                        </div>
                    </div>
                </div>
            </div>`
});