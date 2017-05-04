"use strict";
define(["knockout", "jquery", "escapeHtml", "text!runs/dictionaryBrowser/template.html",
    "runs/dictionaryBrowser/DictEntry"],
    function (ko, $, escapeHtml, htmlTemplate, DictEntry) {
        ko.components.register("dictionary-browser", {
            viewModel: function (params) {
                this.escape = escapeHtml;
                this.dict = new DictEntry("", params.value);
            },
            template: htmlTemplate
        });
    });