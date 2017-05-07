"use strict";
define(["knockout", "escapeHtml", "runs/dictionaryBrowser/DictEntry", "text!runs/dictionaryBrowser/template.html"],
    function (ko, escapeHtml, DictEntry, htmlTemplate) {
        ko.components.register("dictionary-browser", {
            viewModel: function (params) {
                this.escape = escapeHtml;
                this.dict = new DictEntry("", params.value);
            },
            template: htmlTemplate
        });
    });