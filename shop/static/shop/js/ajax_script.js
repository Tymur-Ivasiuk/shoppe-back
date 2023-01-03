//Django AJAX
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//DJANGO AJAX end

const add_to_favorites_url = 'http://127.0.0.1:8000/favorites/add/'
const remove_from_favorites_url = 'http://127.0.0.1:8000/favorites/remove/'
const favorites_api_url = 'http://127.0.0.1:8000/favorites/api/'
const add_to_favorites_class = 'active'

function add_to_favorites() {
    $('#button_like').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault();

            const id = $(el).data('id')

            if ($(el).hasClass(add_to_favorites_class)) {
                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(add_to_favorites_class)
                    }
                })
            } else {
                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(add_to_favorites_class)
                    }
                })
            }
        })
    })
}

function get_favorites() {
    $.getJSON(favorites_api_url, (json) => {
        if (json['liked'] !== null) {
            for(let i=0; i<json['liked'].length; i++) {
                $('#button_like').each((index, el) => {
                    const id = $(el).data('id')
                    if (json['liked'][i] == id) {
                        $(el).addClass(add_to_favorites_class)
                    }
                })
            }
        }
    })
}


const add_cart_url = 'http://127.0.0.1:8000/cart-options/add'
const remove_cart_url = 'http://127.0.0.1:8000/cart-options/remove'
const clear_cart_url = 'http://127.0.0.1:8000/cart-options/clear'

function add_to_cart() {
    $('.product-info_order-button-cart-text').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault();

            $.ajax({
                url: add_cart_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    id: $('#product_id').val(),
                    price: $('#price').val(),
                    quantity: $('#num_count').val(),
                    url_from: $('#url_from').val()
                },
                success: function() {
                    $('#yes-msg').addClass('active-msg');
                    setTimeout(function() {$('#yes-msg').removeClass('active-msg')}, 7000);
                }

            })
        })
    })
}





$(document).ready(function() {
    add_to_cart()
    add_to_favorites()
    get_favorites()
})