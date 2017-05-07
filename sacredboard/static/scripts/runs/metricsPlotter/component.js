"use strict";
define(["knockout", "escapeHtml", "text!runs/metricsPlotter/template.html", "plotly"],
    function (ko, escapeHtml, htmlTemplate, Plotly) {
        ko.components.register("metrics-plot", {
            viewModel: function (params) {
                this.escape = escapeHtml;
                this.x = [];
                this.y = [];
                for (var i = 0; i < 200; i++) {
                    if (i % 3 == 0) {
                        this.x.push(i);
                        this.y.push(i * i / 10);
                    }

                }
            },
            template: htmlTemplate
        });
        ko.bindingHandlers.plot = {
            init: function (element, valueAccessor, allBindings, /*deprecated*/ viewModel, bindingContext) {
                var trace1 = {
                    x: bindingContext.$data.x,
                    y: bindingContext.$data.y,
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