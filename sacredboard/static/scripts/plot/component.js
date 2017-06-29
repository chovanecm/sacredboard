"use strict";
define(["knockout", "escapeHtml", "text!plot/template.html", "plotly"],
    function (ko, escapeHtml, htmlTemplate, Plotly) {
        ko.components.register("plot", {
            viewModel: function (params) {
                var self = this;
                this.escape = escapeHtml;
                this.x = params.x;
                this.y = params.y;
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

                var data = [trace1];
                Plotly.newPlot(element, data);
            },
            update: function (element, valueAccessor) {
                /* empty for now */
            }
        };
    });