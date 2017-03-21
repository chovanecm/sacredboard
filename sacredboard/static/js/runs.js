/**
 * Created by Martin on 22.12.2016.
 */
function scrollDown(obj) {
    $(obj).scrollTop(obj.scrollHeight);
}

/**
 * Generate detail view for an experiment
 * @param run Run returned via the web service
 * @returns {string} HTML representation of the detail
 */
function generate_detail_view(run) {
    // `run` is the original data object for the row
    var tabs = `
            <div class="container-fluid detail-view">
            <div class="row">
                <div class="col-md-2">
                      <ul class="nav nav-pills nav-stacked">
                        <li role="presentation" class="active">
                            <a href="#experiment-config-` + escapeHtml(run.id) + `" data-toggle="pill">Config</a>
                        </li>
                        <li role="presentation">
                            <a href="#captured-output-` + escapeHtml(run.id) + `" data-toggle="pill">Captured output</a>
                        </li>
                        <li role="presentation">
                            <a href="#tensorflow-` + escapeHtml(run.id) + `" data-toggle="pill">Tensorflow logs</a>
                        </li>
                      </ul>
                  </div>
                  <div class="tab-content col-md-10">
                      <div id="experiment-config-` + escapeHtml(run.id) + `" class="tab-pane active table-responsive">
                      <h4>Run configuration</h4>
                      <div class="detail-page-box">
                            <table class="table table-condensed">
                            <caption style="display: none">Run configuration</caption>
                            __CONFIG_PARAMETERS__
                            </table>
                        </div>
                      </div>
                      <div id="captured-output-` + escapeHtml(run.id) + `" class="tab-pane">
                      <h4>Captured output from the experiment</h4>
                        <pre class="scrollDown detail-page-box" sacred-content="captured_out">`
        + escapeHtml(run.object.captured_out) + `</pre>
                      </div>
                      <div id="tensorflow-` + escapeHtml(run.id) + `"  class="tab-pane">
                        <h4>Tensorflow logs</h4>
                        <div class="detail-page-box">
                            __TENSORFLOW_LOGDIRS__
                        </div>
                      </div>
                  </div>
                </div>
            </div>
            `;
    tabs = tabs.replace(/__CONFIG_PARAMETERS__/g, render_config_parameters(run.object.config));
    tabs = tabs.replace(/__TENSORFLOW_LOGDIRS__/g, render_tensorflow_dirs(run.id, run.object.info.tensorflow || {}));
    return tabs;
}


function render_config_parameters(config, config_prefix) {
    if (config_prefix == undefined) {
        config_prefix = "";
    }
    var output = "";
    for (var key in config) {
        if (typeof config[key] == "object") {
            output += render_config_parameters(config[key], key.toString() + ".");
        } else {
            output += "<tr><td>" + escapeHtml(config_prefix + key) + "</td><td>" + escapeHtml(config[key]) + "</td></tr>\n";
        }

    }
    return output;
}

function render_tensorflow_dirs(experimentId, tensorflow) {
    var tensorflow_dirs = tensorflow.logdirs || [];
    if (tensorflow_dirs.length == 0) {
        return "<em>No Tensorflow logs found. See the "
        + "<!--<a href='http://sacred.readthedocs.io/en/latest/tensorflow.html' title='Integration with Tensorflow'>-->"
        + "<a href='https://github.com/IDSIA/sacred/blob/develop/docs/tensorflow.rst' title='Integration with Tensorflow'>"
        + "documentation</a> on integration between Sacred and Tensorflow for more information.</em>";
    }
    var output = `<table class="table table-condensed">
                            <caption style="display: none;">Tensorflow logs</caption>
                            <thead><th>Log directory</th><th></th></thead>\n`;
    for (var key in tensorflow_dirs) {
        output += "<tr><td>" + escapeHtml(tensorflow_dirs[key]) + "</td>"
        + "<td><a href='/tensorboard/start/" + experimentId + "/" + key + "' target='_blank'>Run Tensorboard</a>"
        + "</td></tr>\n";
    }
    output += `</table>`;
    return output;
}
