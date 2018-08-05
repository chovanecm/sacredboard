"use strict";
define(["knockout"], function (ko) {
    /**
     * Decorator that validates user input in QueryFilter.
     *
     * Allows only enquoted "string" or 123.4 number to be inputted and
     * prevents the "regex" operator from being used with numbers.
     *
     * @param {ko.observable} target - The target observable (value holder).
     * @param {QueryFilter} queryFilter - The QueryFilter to be checked.
     * @returns {*} Target.
     */
    ko.extenders.validateJSONValue = function (target, queryFilter) {

        //add some sub-observables to our observable
        target.hasError = ko.observable();
        target.validationMessage = ko.observable();

        //define a function to do validation
        function validate(newValue) {
            var error = false;
            var message = "Enquoted \"string\", number, or d:ISO-Date required.";

            //Check date
            if (newValue.startsWith("d:")) {
                const strDate = newValue.substr(2);
                const date = Date.parse(strDate);
                error = isNaN(date);
            } else {
                // Check strings and numbers
                try {
                    var parsed = JSON.parse(newValue);
                    // only string or numbers
                    if (typeof(parsed) != "string" && typeof(parsed) != "number") {
                        error = true;
                    }

                    if (queryFilter.operator() == "regex" && typeof(parsed) != "string") {
                        error = true;
                        message = "Enquoted \"string\" value required for regular expressions";
                    }
                } catch (ex) {
                    error = true;
                }
            }
            target.hasError(error);
            target.validationMessage(error ? message : "");
        }

        //initial validation
        validate(target());

        //validate whenever the value changes
        target.subscribe(validate);
        queryFilter.operator.subscribe(function () {
            validate(target());
        });

        //return the original observable
        return target;
    };
    return ko.extenders.validateJSONValue;
});
