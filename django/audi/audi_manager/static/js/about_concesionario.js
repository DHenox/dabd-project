$(document).ready(function () {
    var numeroInput = document.getElementById('numero-input');
    var kilometrosSlider = document.getElementById('kilometros-slider');
    var precioSlider = document.getElementById('precio-slider');
    var kilometrosValues = document.getElementById('kilometros-values');
    var precioValues = document.getElementById('precio-values');

    // Inicializar el slider de kilómetros
    noUiSlider.create(kilometrosSlider, {
        start: [0, kilometros[kilometros.length - 1]],
        connect: true,
        range: {
            min: 0,
            max: kilometros[kilometros.length - 1],
        },
        step: 1,
        pips: false,
    });

    // Inicializar el slider de precio
    noUiSlider.create(precioSlider, {
        start: [0, precios[precios.length - 1]],
        connect: true,
        range: {
            min: 0,
            max: precios[precios.length - 1],
        },
        step: 1,
        pips: false,
    });

    // Filtrar por número de exposición
    $(numeroInput).on('input', function () {
        filterExposiciones(
            numeroInput.value.trim(),
            kilometrosSlider.noUiSlider.get()[0],
            kilometrosSlider.noUiSlider.get()[1],
            precioSlider.noUiSlider.get()[0],
            precioSlider.noUiSlider.get()[1]
        );
    });

    kilometrosSlider.noUiSlider.on('update', function (values, handle) {
        var formattedValues = values.map(Math.round);
        kilometrosValues.innerHTML =
            '[ ' + formattedValues[0] + ' - ' + formattedValues[1] + ' ] km';

        filterExposiciones(
            numeroInput.value.trim(),
            kilometrosSlider.noUiSlider.get()[0],
            kilometrosSlider.noUiSlider.get()[1],
            precioSlider.noUiSlider.get()[0],
            precioSlider.noUiSlider.get()[1]
        );
    });

    precioSlider.noUiSlider.on('update', function (values, handle) {
        var formattedValues = values.map(Math.round);
        precioValues.innerHTML =
            '[ ' + formattedValues[0] + ' - ' + formattedValues[1] + ' ] €';
        filterExposiciones(
            numeroInput.value.trim(),
            kilometrosSlider.noUiSlider.get()[0],
            kilometrosSlider.noUiSlider.get()[1],
            precioSlider.noUiSlider.get()[0],
            precioSlider.noUiSlider.get()[1]
        );
    });

    // Función para filtrar las exposiciones según los filtros seleccionados
    function filterExposiciones(
        numero,
        minkilometros,
        maxkilometros,
        minPrecio,
        maxPrecio
    ) {
        $('#exposiciones-list')
            .children()
            .each(function () {
                var exposicionNumero = $(this)
                    .find('.card-title')
                    .text()
                    .trim()
                    .split(':')[1]
                    .trim();
                var exposicionkilometros = parseInt(
                    $(this)
                        .find('.card-text')
                        .eq(0)
                        .text()
                        .trim()
                        .split(':')[1]
                        .trim()
                );
                var exposicionPrecio = parseInt(
                    $(this)
                        .find('.card-text')
                        .eq(1)
                        .text()
                        .trim()
                        .split(':')[1]
                        .trim()
                        .split(' ')[0]
                        .trim()
                );

                var numeroMatches =
                    numero === '' || exposicionNumero.startsWith(numero);
                var kilometrosMatches =
                    minkilometros === undefined ||
                    (exposicionkilometros >= minkilometros &&
                        exposicionkilometros <= maxkilometros);
                var precioMatches =
                    minPrecio === undefined ||
                    (exposicionPrecio >= minPrecio &&
                        exposicionPrecio <= maxPrecio);

                if (numeroMatches && kilometrosMatches && precioMatches) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
    }
});
