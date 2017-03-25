define("runs/filters", ["knockout", "knockoutMapping", "jquery", "text!runs/filters.html", "enquotedStringOrNumberValidator"],
    function (ko, knockoutMapping, $, htmlTemplate, stringOrNumberValidator) {
        ko.mapping = knockoutMapping;
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
                return JSON.parse(this.value());
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
                        this.queryFilters().addFilter(this.filterToAdd().clone());
                    }
                };

                this.filterReadyToAdd = function () {
                    var fieldAndOperatorSet = (this.filterToAdd().field() != "" && this.filterToAdd().operator() != "");
                    return fieldAndOperatorSet && !this.filterToAdd().value.hasError();
                };

                this.filterToAdd().field.subscribe(function () {
                    if (this.filterToAdd().field().startsWith(".")) {
                        this.filterToAdd().field("config" + this.filterToAdd().field());
                    }
                }, this);
            },
            template: htmlTemplate
        });

        return {
            QueryFilter: QueryFilter,
            QueryFilters: QueryFilters
        };
    });
