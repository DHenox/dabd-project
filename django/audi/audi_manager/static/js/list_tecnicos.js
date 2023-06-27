$(document).ready(function () {
    var timer = null;
    var delay = 500;
    $('#nombre-input, #dni-input, #num_tel-input').on('keyup', function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
            $('form.XD').submit();
        }, delay);
    });

    // Handler for especializacion filter change
    $('#especializacion-filter').change(function () {
        // Submit the form to apply the filter
        $('form.XD').submit();
    });
});
