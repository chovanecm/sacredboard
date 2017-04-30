var require = {
     baseUrl: "static/scripts",
    paths: {
        jquery: "../lib/jquery/jquery-3.1.1.min",
        knockout: "../lib/knockout/knockout-min",
        datatables: "../lib/datatables/datatables.min",
        "datatables.net": "../lib/datatables/DataTables-1.10.13/js/jquery.dataTables",
        'datatables-bootstrap' : '../lib/datatables/DataTables-1.10.13/js/dataTables.bootstrap',
        bootstrap: "../lib/bootstrap/js/bootstrap.min"
    },
    shim : {
        "bootstrap" : { "deps" :["jquery"]},
        "datatables": { "deps": ["jquery", "datatables.net", "datatables-bootstrap"]}
    }
};

