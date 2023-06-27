function openForm() {
    document.getElementById("popupForm").style.display = "block";
}
function closeForm() {
    document.getElementById("popupForm").style.display = "none";
}

function logout() {
    window.location.href = '/audi_manager/logout';
}

// When the user clicks anywhere outside of the modal, close it


$(document).ready(function () {
    var timer = null;
    $('#dni-input, #concesionario-input').on(
        'keyup',
        function () {
            clearTimeout(timer);
            timer = setTimeout(function () {
                $('.XD').submit();
            }, 500);
        }
    );

    $('#rating-input').change(function () {
        $('.XD').submit();
    });

    // window.onclick = function (event) {
    //     let modal = document.getElementById('loginPopup');
    //     if (event.target == modal) {
    //         closeForm();
    //     }
    // }
    // convert to jquery cl When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        let modal = document.getElementById('loginPopup');
        if (event.target == modal) {
            closeForm();
        }
    }
});
