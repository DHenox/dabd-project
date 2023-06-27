$(document).ready(function () {
    // Delay between keyup events before triggering the search (in milliseconds)
    var delay = 500;
    var timer = null;

    $('#pais-input, #nombre-input').on('keyup', function () {
        clearTimeout(timer);

        timer = setTimeout(function () {
            $('.XD').submit();
        }, delay);
    });
});

function logout() {
    window.location.href = "/audi_manager/logout";
}


function toggleOrder(event) {
    //var currentOrder = "{{ order }}";
    event.preventDefault();
    console.log("Order:", order);
    var newOrder = order === 'asc' ? 'desc' : 'asc';
    console.log("New order:", newOrder);
    order = newOrder;
    currentUrl = window.location.href;
    var newUrl = updateQueryStringParameter(currentUrl, 'order', newOrder);
    window.location.href = newUrl;
}

function updateQueryStringParameter(uri, key, value) {
    var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
    var separator = uri.indexOf('?') !== -1 ? "&" : "?";
    if (uri.match(re)) {
        return uri.replace(re, '$1' + key + "=" + value + '$2');
    }
    else {
        return uri + separator + key + "=" + value;
    }
}