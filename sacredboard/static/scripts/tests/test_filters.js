/*global QUnit*/ //for eslint to ignore missing QUnit
define(["runs/filters/queryFilter"],
    /**
     *
     * @param {QueryFilter} QueryFilter
     */
    function (QueryFilter) {
        QUnit.module("QueryFilter");

        QUnit.test("Test constructor",
            function (assert) {
                var filter = new QueryFilter("host.hostname", "==", "\"node1\"");
                assert.equal(filter.field(), "host.hostname");
                assert.equal(filter.operator(), "==");
                assert.equal(filter.value(), "\"node1\"");
            });

        QUnit.test("Test read from userInputField",
            function (assert) {
                var filter = new QueryFilter("host.hostname", "==", "\"node1\"");
                assert.equal(filter.userInputField(), ".host.hostname");

                filter = new QueryFilter("config.seed", "==", "\"node1\"");
                assert.equal(filter.userInputField(), "seed");
            });

        QUnit.test("Test write into userInputField",
            function (assert) {
                var filter = new QueryFilter("host.hostname", "==", "\"node1\"");
                assert.equal(filter.field(), "host.hostname");
                filter.userInputField("seed");
                assert.equal(filter.field(), "config.seed");
                assert.equal(filter.userInputField(), "seed");

                filter.userInputField(".host.os");
                assert.equal(filter.field(), "host.os");
                assert.equal(filter.userInputField(), ".host.os");

                filter.userInputField(".config.seed");
                assert.equal(filter.field(), "config.seed");
                assert.equal(filter.userInputField(), ".config.seed");

            });


        QUnit.test("Test native value",
            function (assert) {
                var filter = new QueryFilter("host.hostname", "==", "\"node1\"");
                assert.equal(filter.value(), "\"node1\"");
                assert.equal(filter.nativeValue(), "node1");
                filter.value("0");
                assert.equal(filter.nativeValue(), 0);

                filter.value("12");
                assert.equal(filter.nativeValue(), 12);

                filter.value("3.14");
                assert.equal(filter.nativeValue(), 3.14);

                filter.value("-12");
                assert.equal(filter.nativeValue(), -12);

                filter.value("-3.14");
                assert.equal(filter.nativeValue(), -3.14);

                filter.value("-0");
                assert.equal(filter.nativeValue(), 0);

                filter.value("-0.fail");
                var nativeValue;
                assert.throws(
                    function () {
                        nativeValue = filter.nativeValue();
                    },
                    "The input was a string, but was not enquoted. Got " + nativeValue
                )
            });


        QUnit.test("Test hasError",
            function (assert) {
                var filter = new QueryFilter("host.hostname", "==", "\"node1\"");
                assert.notOk(filter.value.hasError());

                filter.value("0");
                assert.notOk(filter.value.hasError());

                filter.value("12");
                assert.notOk(filter.value.hasError());

                filter.value("3.14");
                assert.notOk(filter.value.hasError());

                filter.value("-12");
                assert.notOk(filter.value.hasError());

                filter.value("-3.14");
                assert.notOk(filter.value.hasError());

                filter.value("-0");
                assert.notOk(filter.value.hasError());

                filter.value("-0.fail");
                assert.ok(filter.value.hasError());

                filter.operator("regex");
                filter.value("\"node1\"");
                assert.notOk(filter.value.hasError());

                filter.value("3.14");
                assert.ok(filter.value.hasError());
            });
    });
