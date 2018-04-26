$(function () {

    var selector = $('#fullscreen');


    if (window.location === window.parent.location) {
        selector.html('<span class="fa fa-compress"></span>');
        selector.attr('href', 'http://bootsnipp.com/mouse0270/snippets/rVnOR');
        selector.attr('title', 'Back To Bootsnipp');
    }
    selector.on('click', function(event) {
        event.preventDefault();
        window.parent.location =  $('#fullscreen').attr('href');
    });
    selector.tooltip();
});