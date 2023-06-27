$(document).ready(function () {

    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    $('#nombre-input').on('keyup', function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('.XD').submit();
        }, delay);
    });

    var currentPath = window.location.pathname;
    var pathElements = currentPath.split('/').filter(function (element) {
        return element.length > 0; // Exclude empty elements
    });

    var pathContainer = $('#path');
    var pathLink = '';

    for (var i = 0; i < pathElements.length; i++) {
        pathLink += '/' + pathElements[i];
        var link = $('<a>', {
            href: pathLink,
            text: pathElements[i]
        });
        pathContainer.append(link);

        if (i !== pathElements.length - 1) {
            pathContainer.append('/');
        }
    }
});

function logout() {
    window.location.href = "/audi_manager/logout";
}