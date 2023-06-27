$(document).ready(function () {
    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    $('#matricula-input, #modelo-input, #bastidor-input').on(
        'keyup',
        function () {
            clearTimeout(timer);

            timer = setTimeout(function () {
                $('.XD').submit();
            }, delay);
        }
    );

    $('#ano-filter').change(function () {
        $('.XD').submit();
    });
});

function logout() {
    window.location.href = '/audi_manager/logout';
}
