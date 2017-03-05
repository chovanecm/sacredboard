/**
 * Created by Martin on 4. 3. 2017.
 */
function QueryFilter(field, operator, value, valueType) {
    this.field = ko.observable(field);
    this.operator = ko.observable(operator);
    this.value = ko.observable(value);
    this.valueType = ko.observable(valueType);

    this.clone = function() {
        return new QueryFilter(this.field(), this.operator(), this.value())
    }

    this.toDto = function() {
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
    }
    self.removeFilter = function () {
        self.filters.remove(this);
    }
}

