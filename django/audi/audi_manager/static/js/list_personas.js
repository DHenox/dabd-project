$(document).ready(function () {
    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    $('#name-input, #dni-input').on('keyup', function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('.XD').submit();
        }, delay);
    });
});

function logout() {
    window.location.href = '/audi_manager/logout';
}
