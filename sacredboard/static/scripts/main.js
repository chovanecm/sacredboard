var require = {
     baseUrl: "static/scripts",
    paths: {
        jquery: "../vendors/jquery/jquery-3.1.1.min",
        knockout: "../vendors/knockout/knockout-min",
        datatables: "../vendors/datatables/datatables.min",
        "datatables.net": "../vendors/datatables/DataTables-1.10.13/js/jquery.dataTables",
        'datatables-bootstrap' : '../vendors/datatables/DataTables-1.10.13/js/dataTables.bootstrap',
        bootstrap: "../vendors/bootstrap/js/bootstrap.min",
        text: "../vendors/text"

    },
    shim : {
        "bootstrap" : { "deps" :["jquery"]},
        "datatables": { "deps": ["jquery", "datatables.net", "datatables-bootstrap"]}
    }
};

