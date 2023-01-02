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
    $('.product-info_buttons-like').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault();

            const id = $(el).data('id')
            console.log(el.classList);

            if ($(el).hasClass(add_to_favorites_class)) {
                console.log('minus')
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
                console.log('plus')
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
                $('.product-info_buttons-like').each((index, el) => {
                    const id = $(el).data('id')
                    console.log(json['liked'][i], id)
                    if (json['liked'][i] == id) {
                        $(el).addClass(add_to_favorites_class)
                    }
                })
            }
        }
    })
}

$(document).ready(function() {
    add_to_favorites()
    get_favorites()
})