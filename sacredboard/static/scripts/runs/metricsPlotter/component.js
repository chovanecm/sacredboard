"use strict";
define(["knockout", "escapeHtml", "text!runs/metricsPlotter/template.html", "plotly"],
    function (ko, escapeHtml, htmlTemplate, Plotly) {
        ko.components.register("metrics-plot", {
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.run = params.run;
                this.values = [];
                this.steps = [];
                this.getMetricList = function () {
                    // The following line returns an empty array if there are no metrics
                    var metrics = (self.run.info || {}).metrics || [];
                    return metrics;

                }
            },
            template: htmlTemplate
        });
        ko.bindingHandlers.plot = {
            init: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                var trace1 = {
                    x: bindingContext.$data.steps,
                    y: bindingContext.$data.values,
                    type: 'scatter'
                };

                var trace2 = {
                    x: [1, 2, 3, 4],
                    y: [16, 5, 11, 9],
                    type: 'scatter'
                };

                var data = [trace1, trace2];
                Plotly.newPlot('plot-graph', data);
            },
            update: function (element, valueAccessor) {
                /* empty for now */
            }
        };
    });