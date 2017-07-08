"use strict";
/**
 * Returns a function that turns a table into a datatable for displaying experiment runs.
 *
 * The module is a candidate for rewriting into knockout.js
 */
define(["bootstrap", "datatable", "datatables-bootstrap", "runs/detailView/component", "jquery", "knockout"],
    function (bootstrap, datatables, dtboostrap, detailView, $, ko) {
        /**
         * Scroll down in the element.
         *
         * @param {DOMNode} obj - The element to be scrolled down.
         */
        function scrollDown(obj) {
            $(obj).scrollTop(obj.scrollHeight);
        }

        /**
         * Turn tableElement into dataTable to display runs.
         *
         * Returns the created table.
         *
         * @param {DOMNode} tableElement - The <table> DOM element representing the table
         * @type {{table: DataTable, reload: function, initTable: function, queryFilter: QueryFiltersDto}}
         */
        var createRunTable = {};
        /**
         * The DataTable object created by the DataTable library.
         * Initially null until initTable is called.
         * @type {DataTable}
         */
        createRunTable.table = null;
        /**
         * Reload the content of the table from server.
         */
        createRunTable.reload = function () {
            createRunTable.table.ajax.reload();
        };
        /**
         * Value of the QueryFilters for the table.
         * When updated, the reload() method must be called to reflect the change.
         *
         * @type QueryFiltersDto
         */
        createRunTable.queryFilter = {type: "and", filters: []};

        /**
         * Initialize DataTable for given element.
         *
         * @param {DOMNode} tableElement - HTML <table> for placing the DataTable.
         */
        createRunTable.initTable = function (tableElement) {
            var jqRuns = $(tableElement);
            /**
             * Configure DataTables
             * @type {{colReorder: boolean, responsive: boolean, bFilter: boolean, deferRender: boolean, serverSide: boolean, ajax: {url: string, data: data}, columns: [*], order: [*]}}
             */
            var config = {
                colReorder: true,
                responsive: false,
                // do not display Datatables filter field
                bFilter: false,

                // Scroller:
                //scrollY: window.innerHeight / 1.4,
                deferRender: true,
                //scroller: false,
                serverSide: true,
                /**
                 * Define the endpoint to read data from
                 * and additional URL parameters to be passed to the backend.
                 */
                ajax: {
                    url: "/api/run",
                    data: function (request) {
                        request.queryFilter = JSON.stringify(createRunTable.queryFilter);

                    }
                },
                "columns": [
                    /**
                     * The +/- column showing whether the experiment run is
                     * expanded to detail view or not.
                     */
                    {
                        "className": "details-control",
                        "orderable": false,
                        "data": null,
                        "defaultContent": ""
                    },
                    {"data": "id", "name": "_id", "visible": true},
                    /**
                     * Attach a coloured state icon to the experiment name.
                     */
                    {
                        "data": "experiment_name",
                        "name": "experiment.name",
                        "render": function (data, type, row) {
                            return "<span sacred-content=\"status-icon\" sacred-status=\"" + row.status +
                                "\" sacred-is-alive=\"" + row.is_alive + "\">&block;</span>  " + data;
                        }
                    },
                    {"data": "command", "name": "command"},
                    {"data": "start_time", "name": "start_time"},
                    {"data": "heartbeat", "name": "heartbeat"},
                    {"data": "hostname", "name": "hostname"},
                    {"data": "result", "name": "result"}
                ],
                /**
                 * Sort by experiment heartbeat
                 */
                order: [["5", "desc"]]
            };
            // Init DataTables
            var table = jqRuns.DataTable(config);
            createRunTable.table = table;
            // Add event listener for opening and closing details
            jqRuns.find("tbody").on("click", "tr", function () {
                var tr = $(this);
                var row = table.row(tr);
                if (row.child.isShown()) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass("shown");
                }
                else {
                    // open detail view
                    if (row.data() == undefined) {
                        // Nothing to do here
                        return;
                    }
                    var id = row.data().id;
                    var loadDetailData = function () {
                        $.ajax({
                            url: "/api/run/" + id
                        }).done(function (data) {
                            if (data.data[0].id != row.data().id) {
                                /* Before this ajax function was called,
                                 the parent row has changed
                                 (belongs to some other experiment because the user applied filter or pagination)
                                 there is nothing to do here. */
                                return;
                            }
                            var detail_view = null;
                            //Show detail view if not shown yet
                            if (!row.child.isShown()) {
                                var detailComponent = $("<detail-view params='run: run, deleteRunHandler: deleteRunHandler'></detail-view>");
                                row.child(detailComponent).show();
                                detail_view = tr[0].nextSibling;
                                ko.applyBindings({
                                    run: data.data[0],
                                    deleteRunHandler: function (id) {
                                        $.ajax({
                                            method: "DELETE",
                                            url: "/api/run/" + id
                                        }).done(function (msg) {
                                            table.row(row).remove().draw();
                                        }).fail(function (jqXHR, textStatus, errorThrown) {
                                            alert("ERROR: Couldn't remove run " + id + "\nDetails: " + jqXHR.responseText + "\nError thrown: " + errorThrown);
                                        });
                                    }
                                }, detail_view);
                            } else {
                                //detail view already shown, update the content.
                                detail_view = tr[0].nextSibling;
                                $(detail_view).find("[sacred-content=\"captured_out\"]").each(function (i, obj) {
                                    obj.innerText = data.data[0].object.captured_out;
                                });
                            }
                            //scroll to the end of captured out
                            $(detail_view).find(".scrollDown").each(function (i, obj) {
                                scrollDown(obj);
                            });
                            //update parent row with current data:
                            row.data(data.data[0]);
                            //set timeOut to refresh the view again in a few seconds
                            setTimeout(function () {
                                if (row.child.isShown()) {
                                    loadDetailData();
                                }
                            }, 5000);
                        });
                        tr.addClass("shown");
                    };
                    loadDetailData();
                }
            });
            return table;
        };
        return createRunTable;
    });
