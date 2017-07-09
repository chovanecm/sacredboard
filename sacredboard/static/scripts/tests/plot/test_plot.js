/*global QUnit*/ //for eslint to ignore missing QUnit


define(["plot/plotlyplot/formatDate"],
    function (formatDate) {
        QUnit.module("FormatDate");

        QUnit.test("Test formatdate",
            function (assert) {
                // This format should be interpreted as local time
                var d = new Date("April 7, 2014 11:14:28.540");
                var result = formatDate(d);
                assert.equal(result, "2014-04-07 11:14:28.540");
            });
    });