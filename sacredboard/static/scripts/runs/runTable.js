/**
 * Returns a function that turns a table into a datatable for displaying experiment runs
 */
define("runs/runTable", ["bootstrap", "datatables", "datatables-bootstrap", "runs/detailView"],
    function (bootstrap, datatables, dtboostrap, generateDetailView) {
        /**
         * Scrolls down in the element
         * @param obj
         */
        function scrollDown(obj) {
            $(obj).scrollTop(obj.scrollHeight);
        }

        /**
         * Turn tableElement into dataTable displaying runs.
         *
         * Returns the created table.
         * @param tableElement
         */
        var createRunTable = {};
        createRunTable.table = null;
        createRunTable.reload = function () {
            createRunTable.table.ajax.reload();
        };
        createRunTable.queryFilter = {type: "and", filters: []};

        createRunTable.initTable = function (tableElement) {
            var jqRuns = $(tableElement);
            var config = {
                colReorder: true,
                responsive: false,
                bFilter: false,

                // Scroller:
                //scrollY: window.innerHeight / 1.4,
                deferRender: true,
                //scroller: false,
                serverSide: true,
                ajax: {
                    url: "/api/run",
                    data: function (request) {
                        request.queryFilter = JSON.stringify(createRunTable.queryFilter);

                    }
                },
                "columns": [
                    {
                        "className": 'details-control',
                        "orderable": false,
                        "data": null,
                        "defaultContent": ''
                    },
                    {
                        "data": "experiment_name",
                        "name": "experiment.name",
                        "render": function (data, type, row) {
                            return '<span sacred-content="status-icon" sacred-status="' + row.status +
                                '" sacred-is-alive="' + row.is_alive + '">&block;</span>  ' + data;
                        }
                    },
                    {"data": "start_time", "name": "start_time"},
                    {"data": "heartbeat", "name": "heartbeat"},
                    {"data": "hostname", "name": "hostname"},
                    {"data": "result", "name": "result"},
                    {"data": "id", "visible": false}
                ],
                order: [["5", "desc"]]
            };
            var table = jqRuns.DataTable(config);
            createRunTable.table = table;
            // Add event listener for opening and closing details
            jqRuns.find('tbody').on('click', 'tr', function () {
                var tr = $(this);
                var row = table.row(tr);
                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    if (row.data() == undefined) {
                        // Nothing to do here
                        return;
                    }
                    var id = row.data().id;
                    var f = function () {
                        $.ajax({
                            url: "/api/run/" + id
                        }).done(function (data) {
                            if (data.data[0].id != row.data().id) {
                                /* Before this ajax function was called,
                                 our parent row has changed (belongs to some other experiment)
                                 there is nothing to do here. */
                                return;
                            }
                            var detail_view = null;
                            //Show detailed view if not shown yet
                            if (!row.child.isShown()) {
                                row.child(generateDetailView(data.data[0])).show();
                                detail_view = tr[0].nextSibling;
                            } else {
                                //udpdate content
                                detail_view = tr[0].nextSibling;
                                $(detail_view).find('[sacred-content="captured_out"]').each(function (i, obj) {
                                    obj.innerText = data.data[0].object.captured_out;
                                });
                            }
                            //scroll to the end of captured out
                            $(detail_view).find(".scrollDown").each(function (i, obj) {
                                scrollDown(obj);
                            });
                            //update parent row with current data:
                            row.data(data.data[0]);
                            //set timeOut
                            setTimeout(function () {
                                if (row.child.isShown()) {
                                    f();
                                }
                            }, 5000);
                        });
                        tr.addClass('shown');
                    };
                    f();
                }
            });
            return table;
        };
        return createRunTable;
    });
