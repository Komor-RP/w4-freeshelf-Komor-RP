function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$('.favorite').off().on( "click", function(){
    $.ajax({
        type: "POST",
        url: "/favorite_book/",
        data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': csrftoken},
        dataType: "json"})
        .done(function(response) {
            if (response[0] === "added") {
                addLike(response[1])
            } else if (response[0] === "removed") {
                removeLike(response[1])
            }
        })
        .fail(function(rs, e) {
            console.log(rs.responseText);
        });
    
    
});


function addLike(slug) {
    var favorites = parseInt($(`span#${slug}`).text());
    $(`span#${slug}`).html(`${favorites + 1}`);
    $(`[name=${slug}]`).html(`<i class="fas fa-thumbs-up"></i> Remove`); 
}
function removeLike(slug) {
    var favorites = parseInt($(`span#${slug}`).text());
    $(`span#${slug}`).html(`${favorites - 1}`); 
    $(`[name=${slug}]`).html(`<i class="fas fa-thumbs-up"></i> Favorite`); 
}

var sort_buttons = $('.sort-buttons .button');
$(sort_buttons).off().on( "click", function() {
    var query = $(this).attr("name");
    
    $.ajax({
        type: "GET",
        data: {"sort_method" : query},
        url: "/sort_books/"})
        .done(function(response) {
            $('.book-shelf').detach();
            $('body').append(response);
        })
        .fail(function(rs, e) {
            console.log(rs.responseText);
        });
    
});

var suggestionButtons = $('button.suggestion');
$(suggestionButtons).off().on("click", function() {
    var confirmation = $(this).attr("id");
    var bookSlug = $(this).attr("name");

    $.ajax({
        type: "POST",
        url: "/handle_suggestion/",
        data: {
            'confirmation': confirmation,
            'book-slug': bookSlug,
            'csrfmiddlewaretoken': csrftoken
        },
        dataType: "json"})
        .done(function(response) {
            var bookBlock = $(`[name=${bookSlug}]`).parent().parent();
            bookBlock.detach();
        })
        .fail(function(rs, e) {
            console.log("error");
            console.log(rs.responseText);
        });
});
