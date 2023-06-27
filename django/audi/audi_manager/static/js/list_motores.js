$(document).ready(function () {
    // Inicializar el slider

    var potenciaSlider = document.getElementById('potencia-slider');
    var potenciaValues = document.getElementById('potencia-values');
    var selectedCombustible = ''; // Variable para almacenar el filtro de combustible

    noUiSlider.create(potenciaSlider, {
        start: [potencias[0], potencias[potencias.length - 1]],
        connect: true,
        range: {
            'min': potencias[0],
            'max': potencias[potencias.length - 1]
        },
        step: 20,
        pips: false
    });

    potenciaSlider.noUiSlider.on('update', function (values, handle) {
        var formattedValues = values.map(Math.round);
        potenciaValues.innerHTML = '[ ' + formattedValues[0] + ' - ' + formattedValues[1] + ' ] HP';
        filterMotores(selectedCombustible, formattedValues[0], formattedValues[1]);
    });

    // Filtrar por combustible
    $('#combustible-filter').change(function () {
        selectedCombustible = $(this).val();
        var potenciaSliderValues = potenciaSlider.noUiSlider.get();
        filterMotores(selectedCombustible, potenciaSliderValues[0], potenciaSliderValues[1]);
    });

    // Función para filtrar los motores según el combustible y la potencia
    function filterMotores(combustible, minPotencia, maxPotencia) {
        $('#motores-list').children().each(function () {
            var motorCombustible = $(this).find('.card-title').text().trim().split(':')[1].trim();
            var motorPotencia = parseInt($(this).find('.card-text').text().trim().split(':')[1].trim());

            if ((combustible === '' || motorCombustible === combustible) &&
                motorPotencia >= minPotencia && motorPotencia <= maxPotencia) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});
