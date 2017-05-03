"use strict";
define(["knockout", "jquery", "escapeHtml", "text!runs/dictionaryBrowser.html"],
    function (ko, $, escapeHtml, htmlTemplate) {
        ko.components.register("dictionary-browser", {
            viewModel: function (params) {
                this.dict = new DictEntry("", params.value);
                this.escape = escapeHtml;

                function DictEntry(name, value) {
                    var self = this;
                    this.hasChildren = function () {
                        return typeof value == "object";
                    };
                    this.getChildren = function () {
                        if (self.hasChildren()) {
                            var arr = [];
                            for (var valKey in value) {
                                arr.push(new DictEntry(valKey, value[valKey]));
                            }
                            return arr;
                        } else {
                            return [];
                        }
                    };
                    this.getDisplayName = function () {
                        return name;
                    };
                    this.getDisplayValue = function () {
                        if (value instanceof Array) {
                            return value.join(", ");
                        } else {
                            return value.toString();
                        }
                    };
                }
            },
            template: htmlTemplate
        });
    });