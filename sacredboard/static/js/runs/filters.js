/**
 * Created by Martin on 4. 3. 2017.
 */
/**
 *
 * @param field
 * @param operator
 * @param value
 * @constructor
 */
function QueryFilter(field, operator, value) {
    this.field = ko.observable(field);
    this.operator = ko.observable(operator);
    this.value = ko.observable(value).extend({validateJSONValue: this});
    this.nativeValue = ko.pureComputed(function () {
        return  JSON.parse(this.value());
    }, this);
    this.clone = function () {
        return new QueryFilter(this.field(), this.operator(), this.value())
    };

    this.toDto = function () {
        return ko.mapping.toJS({"field": this.field(), "operator": this.operator(), "value": this.nativeValue()});
    };

    this.addParentObserver = function (observer) {/* Do nothing, we consider a QueryFilter to be used as immutable object */
    };
}


ko.extenders.validateJSONValue = function(target, queryFilter) {
    //add some sub-observables to our observable
    target.hasError = ko.observable();
    target.validationMessage = ko.observable();

    //define a function to do validation
    function validate(newValue) {
        var error = false;
        var messages = [];
        try {
            var parsed = JSON.parse(newValue);
            // only string or numbers
            if (typeof(parsed) != "string" && typeof(parsed) != "number") {
                error = true;
                message = "Enquoted \"string\" or number required.";
            }

            if (queryFilter.operator() == "regex" && typeof(parsed) != "string") {
                error = true;
                message = "Enquoted \"string\" value required for regular expressions";
            }
        } catch (ex) {
            error = true;
                message = "Enquoted \"string\" or number required.";
        }
        target.hasError(error);
        target.validationMessage(error ? message : "");
    }

    //initial validation
    validate(target());

    //validate whenever the value changes
    target.subscribe(validate);
    queryFilter.operator.subscribe(function () {validate(target());});

    //return the original observable
    return target;
};

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
            var fieldAndOperatorSet = (this.filterToAdd().field() != "" && this.filterToAdd().operator() != "");
            return fieldAndOperatorSet && !this.filterToAdd().value.hasError();
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
                <div class="form-group " data-bind="css: {'has-error': filterToAdd().value.hasError}">
                    <label class="sr-only" for="queryValue">Query value</label>
                    <input type="text" class="form-control" id="queryValue" placeholder='"string" or 123.4' data-bind="value: filterToAdd().value,
                                                                                                       valueUpdate: 'afterkeydown'">
                </div>
                <!--<div class="form-group">
                    <label class="sr-only" for="queryvalueType">Treat as</label>
                    <select id="queryvalueType" class="form-control" data-bind="options: queryFilters().valueTypes,
                                                                           value: filterToAdd().valueType"></select>
                </div> -->
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
                            <span data-bind="text: value"></span>
                            <a href="#" data-bind="click: $parent.removeFilter">[X]</a>
                        </div>
                    <!-- /ko -->
                    </div>
                </div>
            </div>`
});
