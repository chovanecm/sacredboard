/*global QUnit*/ //for eslint to ignore missing QUnit
var entityMap = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;",
    "/": "&#x2F;",
    "`": "&#x60;",
    "=": "&#x3D;"
};

define(["escapeHtml"], function (replace) {
    QUnit.module("EscapeHTML");

    QUnit.test("Test escaping &, <,>",
        function (assert) {
            assert.equal(replace("hello&<>world"),
                "hello" + entityMap["&"] + entityMap["<"] + entityMap[">"] + "world");
        });

    QUnit.test("Test escaping \", ', /",
        function (assert) {
            assert.equal(replace("hello\"world'/"),
                "hello" + entityMap["\""] + "world" + entityMap["'"] + entityMap["/"]);
        });

    QUnit.test("Test escaping ` and =",
        function (assert) {
            assert.equal(replace("hello`world="),
                "hello" + entityMap["`"] + "world" + entityMap["="]);
        });
});
