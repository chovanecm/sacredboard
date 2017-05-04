"use strict";
define(["knockout", "jquery", "escapeHtml", "text!runs/dictionaryBrowser.html"],
    function (ko, $, escapeHtml, htmlTemplate) {
        ko.components.register("dictionary-browser", {
            viewModel: function (params) {
                this.escape = escapeHtml;
                this.dict = new DictEntry("", params.value);

                function DictEntry(name, value) {
                    var self = this;
                    this.value = value;
                    this.contentCollapsed = ko.observable(true);
                    this.toggleCollapse = function () {
                        if (self.hasChildren()) {
                            self.contentCollapsed(!self.contentCollapsed());
                        }
                    };
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
                            return "[" + value.join(", ") + "]";
                        } else {
                            return value.toString();
                        }
                    };

                    this.content = value;
                }
                DictEntry.prototype.EMPTY = "";
            },
            template: htmlTemplate
        });
    });