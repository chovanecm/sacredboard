"use strict";
/**
 * The module implements the {@link Plot} interface to be used with the Plot.ly library.
 *
 * @module
 */
define(
    [
        "../plot",
        "plotly",
        "./convertDataPoints",
        "command"],
    function (Plot,
              Plotly,
              convertDataPoints,
              CommandQueue) {

        /**
         * Implementation of the {@link Plot} interface with the Plot.ly library.
         */
        class PlotlyPlot extends Plot {
            constructor(element) {
                super(element);
                this._plotted = false;
                this._layout = {showlegend: true};
                this._traces = [];
                this._commandQueue = new CommandQueue();
            }

            plot() {
                if (!this._plotted) {
                    if (this._traces == 0) {
                        // Temporarily add a dummy trace to prevent error in Plotly.
                        this.addTrace([0],[0], "DEFAULT");
                        // And remove it after plotting it
                        var self = this;
                        this._commandQueue.addCommand(function () {
                            self.removeTrace("DEFAULT");
                        });
                    }
                    var copyOfTraces = Array.from(this._traces);
                    Plotly.newPlot(this._element, copyOfTraces, this._layout);
                    this._plotted = true;
                    this._commandQueue.runCommands();
                }
            }

            set xLabel(xLabel) {
                super.xLabel = xLabel;
                this._relayout({"xaxis.title": xLabel});
            }

            set yLabel(yLabel) {
                super.yLabel = yLabel;
                this._relayout({"yaxis.title": yLabel});
            }

            set xType(xType) {
                super.xType = xType;
                this._relayout({"xaxis.type": xType});
            }

            set yType(yType) {
                super.yType = yType;
                this._relayout({"yaxis.type": yType});
            }

            addTrace(x, y, label) {
                var index = this._findTraceIndex(label);
                if (index >= 0) {
                    // A trace with this label is already there.
                    throw new Plot.TraceAlreadyPresentException(label);
                }
                var trace = {
                    x: convertDataPoints(x),
                    y: convertDataPoints(y),
                    type: "scatter",
                    //visible: "legendonly",
                    name: label
                };
                this._traces.push(trace);
                if (this._plotted) {
                    Plotly.addTraces(this._element, trace);
                }
            }

            removeTrace(label) {
                var index = this._findTraceIndex(label);
                if (index < 0) {
                    throw new Plot.TraceNotFoundException(label);
                }
                this._traces.splice(index, 1);
                if (this._plotted) {
                    Plotly.deleteTraces(this._element, index);
                }
            }

            _findTraceIndex(label) {
                return this._traces.findIndex(function (trace) {
                    return trace.name == label;
                });
            }


            _relayout(layout) {
                if (this._plotted) {
                    Plotly.relayout(this._element, layout);
                } else {
                    // When the chart has not yet been plotted, deffer the update.
                    this._commandQueue.addCommand(function () {
                        this._relayout(layout);
                    });
                }

            }

        }
        return PlotlyPlot;
    });