/* Javascript for ReplXBlock. */
function ReplXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    pypyjs.rootUrl = runtime.handlerUrl(element, 'get_file') + 'file=';

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "GET",
            url: window.getFileUrl,
            data: {"file": "modules/index.json"},
            success: updateCount
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
