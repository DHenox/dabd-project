$(document).ready(function () {
    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    $('#num_tel-input, #numero-input').on('keyup', function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('form.XD').submit();
        }, delay);
    });
});
