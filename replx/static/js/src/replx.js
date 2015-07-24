
function ReplXBlock(runtime, element) {

    // DOM Elements
    var themeSelector = $('#theme-selector')[0];
    var editorTextArea = $('#editor-text-area')[0];
    var editor = null;

    // State
    var textChanged = false;
    var loadedThemes = [];

    // Utility functions

    function postAJAX(endpoint_name, data_dict, async, callback) {
        if (typeof async == 'undefined') {
            async = true;
        }
        if (typeof callback == 'undefined') {
            callback = function () {}
        }

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, endpoint_name),
            async: async,
            data: JSON.stringify(data_dict)
        }).done(callback);
    }

    function saveEditorText(async) {
        // TODO: Do we want to add error handling?
        postAJAX('save_editor_text', { "editorText": editor.getValue() }, async);
    }

    // Code to be executed on page load
    $(function ($) {

        // Get variables
        var params = JSON.parse($('#params-json')[0].innerHTML);

        // Set up editor
        editor = CodeMirror.fromTextArea(editorTextArea, {
            lineNumbers: true,
            mode: "python",
            theme: params["themeName"]
        });
        window._e = editor; // TODO: remove this

        // Handle text changing & saving
        setTimeout(function () {
            if (textChanged) {
                saveEditorText(true);
                textChanged = false;
            }
        }, 5000);
        editor.on("change", function (changeObj) { textChanged = true;});
        window.onbeforeunload = function (e) {
            saveEditorText(false);
            return null;
        };

        // Set up REPL
        var repl = createPythonREPL(params["themeName"]);

        // Theme selection
        themeSelector.value = params["themeName"];
        loadedThemes.push(params["themeName"]);
        $("#theme-selector").change(function () {
            var themeName = themeSelector.value;
            var themeIsLoaded = loadedThemes.indexOf(themeName) >= 0;
            postAJAX(
                'change_theme',
                { "themeName": themeName, "getCSS": !themeIsLoaded },
                true,
                function (data) {
                    if (!themeIsLoaded) {
                        var style = document.createElement('style');
                        style.type = 'text/css';
                        style.innerHTML = data['themeCSS'];
                        $('head')[0].appendChild(style);
                        loadedThemes.push(themeName);
                    }
                    editor.setOption('theme', themeName);
                    repl.setTheme(themeName);
                }
            );
        })
    });
}
