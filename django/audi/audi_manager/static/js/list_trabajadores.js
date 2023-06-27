$(document).ready(function () {
    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    // Handler for DNI input change
    // Handler for name input change
    $('#dni-input, #name-input').on('keyup', function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('form.XD').submit();
        }, delay);
    });

    $('#disponibilidad-filter, tipo-trabajador-filter').change(function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('form.XD').submit();
        }, delay);
    });

    // Handler for disponibilidad filter change
    $('#disponibilidad-filter').change(function () {
        $('form.XD').submit();
    });

    // Handler for tipo trabajador filter change
    $('#tipo-trabajador-filter').change(function () {
        $('form.XD').submit();
    });
});

function logout() {
    window.location.href = '/audi_manager/logout';
}
