
function ReplXBlock(runtime, element) {

    var saveEditorTextUrl = runtime.handlerUrl(element, 'save_editor_text');

    $(function ($) {

        /* Code to be executed on page load */

        var editorTextArea = $('#editor-text-area')[0];
        var editor = CodeMirror.fromTextArea(editorTextArea);
        editor.lineNumbers = true;
        editor.mode = "python";
        var textChanged = false;

        function saveEditorText(async) {
            // TODO: Do we want to add error handling?
            $.ajax({
                type: "POST",
                url: saveEditorTextUrl,
                async: async,
                data: JSON.stringify({ "editorText": editor.getValue()})
            })
        }

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
        }
    });
}
