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
            var self = this;
            /* In accordance with https://github.com/chovanecm/sacredboard/issues/8
             the user searches by default in the config scope.
             He may, however, search everywhere if he prepends "." to the beginning
             of the query, e.g. ".host.hostname"
             */
            var defaultScope = "config.";
            this.userInputField = ko.observable("");
            // Search in config. or in the whole run?
            this.fieldScope = ko.pureComputed(function () {
                if (self.userInputField().startsWith(".")) {
                    return "";
                } else {
                    return defaultScope;
                }
            }, this);
            this.field = ko.pureComputed({
                read: function () {
                    if (self.userInputField().startsWith(".")) {
                        return self.userInputField().substring(1);
                    } else if (self.userInputField() != "") {
                        return self.fieldScope() + self.userInputField();
                    } else {
                        return "";
                    }
                },
                /**
                 * @param value String
                 */
                write: function (value) {
                    if (value.startsWith(defaultScope)) {
                        // Set the user input field without the default scope name
                        self.userInputField(value.substring(defaultScope.length));
                    } else if (value != "") {
                        self.userInputField("." + value);
                    } else {
                        self.userInputField("");
                    }
                }
            });
            this.field(field);
            this.operator = ko.observable(operator);
            this.value = ko.observable(value).extend({validateJSONValue: this});
            this.nativeValue = ko.pureComputed(function () {
                return JSON.parse(this.value());
            }, this);

            this.clone = function () {
                return new QueryFilter(this.field(), this.operator(), this.value())
            };

            this.toDto = function () {
                return ko.mapping.toJS({
                    "field": this.field(),
                    "operator": this.operator(),
                    "value": this.nativeValue()
                });
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

                // this.filterToAdd().field.subscribe(function () {
                //     /**
                //      * To comply with Use Case UC 1 (described in Martin Chovanec's Master's thesis)
                //      * the user search by default in the config. scope
                //      */
                //     if (this.filterToAdd().field().startsWith(".")) {
                //         this.filterToAdd().fieldScope("");
                //     } else {
                //         this.filterToAdd().fieldScope("config.");
                //     }
                // }, this);
            },
            template: htmlTemplate
        });

        return {
            QueryFilter: QueryFilter,
            QueryFilters: QueryFilters
        };
    });
