"use strict";
define(["knockout"], function (ko) {
    /**
     * Decorator that validates user input in QueryFilter.
     *
     * Allows only enquoted "string" or 123.4 number to be inputted and
     * prevents the "regex" operator from being used with numbers.
     * @param target - The target observable (value holder).
     * @param {QueryFilter} queryFilter - The QueryFilter to be checked.
     * @returns {*} target
     */
    ko.extenders.validateJSONValue = function (target, queryFilter) {

        //add some sub-observables to our observable
        target.hasError = ko.observable();
        target.validationMessage = ko.observable();

        //define a function to do validation
        function validate(newValue) {
            var error = false;
            var message;
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
        queryFilter.operator.subscribe(function () {
            validate(target());
        });

        //return the original observable
        return target;
    };
    return ko.extenders.validateJSONValue;
});
