/**
 * Created by Martin on 4. 3. 2017.
 */
function QueryFilter(field, operator, value) {
    this.field = ko.observable(field);
    this.operator = ko.observable(operator);
    this.value = ko.observable(value);

    this.clone = function() {
        return new QueryFilter(this.field(), this.operator(), this.value())
    }
}

function QueryFilters() {
    let self = this;
    this.filters = ko.observableArray([]);
    this.operators = ['==', '!=', '<', '<=', '>', '>=', 'contains'];

    self.addFilter = function (filter) {
        self.filters.push(filter);
    }
    self.removeFilter = function () {
        self.filters.remove(this);
    }
}
