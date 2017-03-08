/**
 * Created by Martin on 4. 3. 2017.
 */
/**
 *
 * @param field
 * @param operator
 * @param value
 * @param {string} valueType optional 'string' or 'number' (default: determined by the value)
 * @constructor
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
        var targetValue = this.value();
        if (this.valueType() != undefined) {
            targetValue = (this.valueType() == "number") ? Number(this.value()) : this.value();
        }
        return ko.mapping.toJS({"field": this.field(), "operator": this.operator(), "value": targetValue});
    };

    this.addParentObserver = function (observer) {/* Do nothing, we consider a QueryFilter to be used as immutable object */
    };
}
/**
 *
 * @param type either 'and' or 'or'. Default: 'and'
 * @param filters an array of terms. either
 * @constructor
 */
function QueryFilters(type, filters) {
    var self = this;
    this.filters = ko.observableArray(filters == undefined ? [] : filters);
    this.filters.extend({notify: 'always'});
    this.operators = ['==', '!=', '<', '<=', '>', '>=', 'regex'];
    this.valueTypes = ['string', 'number'];
    this.type = ko.observable(type == undefined ? 'and' : type);
    self.addFilter = function (filter) {
        self.filters.push(filter);
        filter.addParentObserver(self.filters);
    };
    self.removeFilter = function (filter) {
        self.filters.remove(filter);

    };
    self.toDto = function () {
        return ko.mapping.toJS(
            {
                type: self.type(),
                filters: $.map(self.filters(),
                    function (filter) {
                        return filter.toDto()
                    })
            });
    };
    self.addParentObserver = function (observer) {
        //Note: The observer must be set to always notify subscribers even if it doesn't detect a change.
        self.filters.subscribe(function () {
            observer.notifySubscribers();
        });
    };
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
                    <div data-bind="foreach: {data: filters, as: 'filter'}">
                    <!-- ko if: filter['field'] != undefined -->
                    <!-- this can only display simple filters -->
                        <div class="query-filter">
                            <span data-bind="text: field"></span>
                            <span data-bind="text: operator"></span>
                            <span data-bind="visible: valueType() == 'string'">"</span><span data-bind="text: value"></span><span data-bind="visible: valueType() == 'string'">"</span>
                            <a href="#" data-bind="click: $parent.removeFilter">[X]</a>
                        </div>
                    <!-- /ko -->
                    </div>
                </div>
            </div>`
});
