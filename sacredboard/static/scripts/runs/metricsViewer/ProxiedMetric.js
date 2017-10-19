/**
 * Adds support for lazy-loading metrics from the backend.
 *
 * Issue: https://github.com/chovanecm/sacredboard/issues/59
 * @module
 */
define(["runs/Metric", "knockout", "jquery"], function (Metric, ko, $) {
    "use strict";
    /**
     * Adds support for lazy-loading metrics from the backend.sudo s
     *
     * Issue: https://github.com/chovanecm/sacredboard/issues/59
     */
    class ProxiedMetric extends Metric {
        constructor(name, runId, metricId) {
            super(name, ko.observableArray(), ko.observableArray(), ko.observableArray());
            this._runId = runId;
            this._metricId = metricId;
            this._fetched = false;
            this._fetchingInProgress = false;
            this._timestamps = ko.observableArray();
            this._steps = ko.observableArray();
            this._values = ko.observableArray();
        }

        get timestamps() {
            if (!this._fetched) {
                this.fetch();
            }
            return this._timestamps;
        }

        set timestamps(val) {
            this._timestamps = val;
        }

        get steps() {
            if (!this._fetched) {
                this.fetch();
            }
            return this._steps;
        }

        set steps(val) {
            this._steps = val;
        }

        get values() {
            if (!this._fetched) {
                this.fetch();
            }
            return this._values;
        }

        set values(val) {
            this._values = val;
        }

        fetch() {
            if (this._fetchingInProgress) {
                return;
            }
            var self = this;
            this._fetchingInProgress = true;
            $.getJSON("api/run/" + this._runId + "/metric/" + this._metricId,
                function (data) {
                    self._values(data["values"]);
                    self._steps(data["steps"]);
                    self._timestamps(data["strtimestamps"].map(function (d) {
                        return new Date(d);
                    }));
                    self._fetched = true;
                    self._fetchingInProgress = false;
                }).fail(function (jqxhr, textStatus, error) {self.onLoadFail(textStatus, error, self.name());});
        }

        /**
         * Trigger when the metric couldn't be loaded.
         *
         * @param {string} textStatus - Status returned by the HTTP request.
         * @param {string} error - Error type returned by the HTTP request.
         * @param {string} name - Name of the metric that have failed to load.
         */
        onLoadFail(textStatus, error, name)  {
            /* override the method if possible */
            alert("Error when loading metric " + name + ".\nError message: " + textStatus + "\nError:" + error);
        }

    }
    return ProxiedMetric;
});