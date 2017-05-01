var requirejs = require("./r.js");
requirejs.config({
    baseUrl: __dirname + "/..",
    nodeRequire: require,
    paths: {
        jquery: "../lib/jquery/jquery-3.1.1.min",
        knockout: "../lib/knockout/knockout-min",
        datatables: "../lib/datatables/datatables.min",
        "datatables.net": "../lib/datatables/DataTables-1.10.13/js/jquery.dataTables",
        'datatables-bootstrap': '../lib/datatables/DataTables-1.10.13/js/dataTables.bootstrap',
        bootstrap: "../lib/bootstrap/js/bootstrap.min"
    },
    shim: {
        "bootstrap": {"deps": ["jquery"]},
        "datatables": {"deps": ["jquery", "datatables.net", "datatables-bootstrap"]}
    }
});
/**
 @typedef {{async:async, equal:equal, deepEqual:deepEqual, notEqual:notEqual, notOk:notOk, ok:ok, throws:throws}} QAssert
 */

requirejs(["test_filters.js"], function (filters) {
});