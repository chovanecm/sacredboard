var require = {
     baseUrl: "static/scripts",
    paths: {
        jquery: "../lib/jquery/jquery-3.1.1.min",
        knockout: "../lib/knockout/knockout-min",
        knockoutMapping: "../lib/knockout/knockout.mapping-latest",
        datatables: "../lib/datatables/datatables.min",
        bootstrap: "../lib/bootstrap/bootstrap.min"
    },
    shim : {
        "bootstrap" : { "deps" :["jquery"] },
        "datatables" : { "deps": ["jquery","bootstrap"]},
        "knockoutMapping" : { "deps": ["knockout"]}
    }
};

