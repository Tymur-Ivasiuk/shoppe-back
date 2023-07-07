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

const baseUrl = window.location.origin + "/cart-options/"

const add_cart_url = baseUrl + "add'
const remove_cart_url = baseUrl + "remove'
const json_cart_url = baseUrl + "json'

function add_to_cart() {
    $('button[name="quantity"]').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault();

            const max_value = Number($(el).parent('div.cart-item-amount').find('#num_count').attr('max'))
            const id = Number($(el).parent('div.cart-item-amount').parent('form').find('#product_id').val())
            const num_count = $(el).parent('div.cart-item-amount').find('#num_count')

            $.ajax({
                url: add_cart_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    id: id,
                    quantity: $(el).val(),
                    url_from: $('#url_from').val()
                },
                success: function() {
                    num_count.val(Number(num_count.val())+Number($(el).val()))
                    checkAjax()
                    if (Number(num_count.val()) >= max_value) {
                        console.log('MANY')
                        $('button[name="quantity"].button_plus').filter(`[product-id=${id}]`).addClass('disabled')
                        $('button[name="quantity"].button_plus').filter(`[product-id=${id}]`).attr('disabled', 'true')
                    } else {
                        $('button[name="quantity"].button_plus').filter(`[product-id=${id}]`).removeClass('disabled')
                        $('button[name="quantity"].button_plus').filter(`[product-id=${id}]`).removeAttr('disabled')
                    }

                    if(Number(num_count.val()) == 0) {
                        $(el).parents('div.cart-item').filter(`[product-id=${id}]`).remove()
                    }

                }
            })
        })
    })
}

function removeFromCart() {
    $('.button-remove').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault();

            const id = $(el).parent('form').find('input[name="id"]').val()

            $.ajax({
                url: remove_cart_url,
                type: 'POST',
                dataType: 'json',
                data: {
                    id: id,
                    url_from: $('#url_from').val()
                },
                success: function() {
                    checkAjax()
                    $(el).parents('div.cart-item').filter(`[product-id=${id}]`).remove()
                }
            })
        })
    })
}

function checkAjax() {
    $.getJSON(json_cart_url, (json) => {
        if (json !== null) {
            let sum = 0
            Object.keys(json).forEach(function(key) {
                sum += Number(json[key]['price'])*Number(json[key]['quantity']);
            });
            if (sum == 0){
                location.reload()
            } else {
                $('#subtotal').html(sum)
                $('#total').html(sum+Number($('#shipping').html()))
            }
        }
    })

}


$(document).ready(function() {
    console.log()
    add_to_cart()
    removeFromCart()
})