function openForm() {
    document.getElementById("popupForm").style.display = "block";
}
function closeForm() {
    document.getElementById("popupForm").style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    let modal = document.getElementById('addClientePopup');
    if (event.target == modal) {
        closeForm();
    }
}

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

    //when the user selects exposicion from the dropdown edit the option value from concesionario to match the exposicion.concesionario
    $('#concesionario').change(function () {
        var concesionario = document.getElementById("concesionario").value;
        console.log('CONCESIONARIO', concesionario);
        document.getElementById("concesionario2").value = concesionario;
        var url = '/audi_manager/get_exposicion/' + concesionario;
        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'text',
            success: function (data) {
                var exposicion = data;
                console.log('EXPOSICION', exposicion);
                exposicion = exposicion.split(',');
                var selectexposicion = document.getElementById("exposicion");
                selectexposicion.options.length = 0;
                for (var i = 0; i < exposicion.length; i++) {
                    var opt = exposicion[i];
                    var el = document.createElement("option");
                    el.textContent = opt;
                    el.value = opt;
                    selectexposicion.appendChild(el);
                }

                var url = '/audi_manager/get_comercial/' + concesionario;

                $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'text',
                    success: function (data2) {
                        var comercials = data2;
                        comercials = comercials.split(',');
                        console.log('COMERCIALES', comercials);
                        var select = document.getElementById("comercial");
                        select.options.length = 0;
                        for (var i = 0; i < comercials.length; i++) {
                            var opt = comercials[i];
                            var el = document.createElement("option");
                            el.textContent = opt;
                            el.value = opt;
                            select.appendChild(el);
                        }
                    }
                });
            }

        });

        // change the comercial select options to match the comercials from the selected concesionario


        // function addVehiculo() {
        //     var selectedVehiculo = document.getElementById("vehiculo_add").value;
        //     var url = '/audi_manager/add_vehiculo/' + selectedVehiculo + '/' + dni_tecnico;
        //     window.location.href = url;
        // }
    });
});