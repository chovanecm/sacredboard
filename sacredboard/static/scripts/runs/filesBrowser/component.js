"use strict";
define(["knockout", "text!runs/filesBrowser/template.html"],
    function (ko, htmlTemplate) {
        ko.components.register("files-browser", {
            viewModel: function (params) {
                var self = this;
                this.run_id = params.run_id;
                this.files = params.files;
                this.url_all = params.all_url;
                this.files = [];

                // sources files just are arrays. convert to objects here
                params.files.forEach((element, index, array) => {
                    if (Array.isArray(element)) {
                        this.files.push({name: element[0], file_id: element[1]});
                    }
                    else {
                        // just pass through
                        this.files.push(element);
                    }
                });

                this.downloadFile = function (file) {
                    window.location.href = `api/file/${file.file_id.$oid}`;
                };

                this.downloadFileAll = function (vm) {
                    window.location.href = this.url_all + vm.run_id;
                };
            },
            template: htmlTemplate
        });
    });