/*eslint no-unused-vars: 0*/
var require = {
    baseUrl: "static/scripts",
    paths: {
        jquery: "../vendors/jquery/jquery-3.1.1.min",
        knockout: "../vendors/knockout/knockout-min",
        "datatable": "../vendors/datatables/datatables.min",
        "datatables.net": "../vendors/datatables/DataTables-1.10.15/js/jquery.dataTables",
        "datatables-bootstrap" : "../vendors/datatables/DataTables-1.10.15/js/dataTables.bootstrap",
        bootstrap: "../vendors/bootstrap/js/bootstrap.min",
        "text": "../vendors/text"

    },
    shim : {
        "bootstrap" : { "deps" :["jquery"]},
        "datatables": { "deps": ["jquery", "datatables.net", "datatables-bootstrap"]}
    }
};