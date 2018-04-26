/**
 * setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.
 * http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
 */
function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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
$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
$(document).ready(function() {

    var $body = $('body'),
    basics = {pageSize: 10, pageIndex: 1, sortField: '-created_at'};
    $('#workinprogress').hide();

    fetchListing(basics);

    $('#listing_searchform').submit(function(event){
        event.preventDefault();
        $('#preloader').hide();
        var forminfo = $(this).serializeArray().reduce(function(a, x) { a[x.name] = x.value; return a; }, {});
        basics['search'] = true;
        const allRules = Object.assign(forminfo, basics);
        //$.each($(this).serializeArray(), function (i, field) { form[field.name] = field.value || ""; });
        fetchListing(allRules);
    });

    $('.listingform').submit(function(event) {
        event.preventDefault();
        $('#workinprogress').show();
    });

    $body.on('click', 'a.alink', function(event) {
        event.preventDefault();
        console.log('#####HREF ', $(this).attr('href'));
        basics['filter'] = $(this).data('filter');
        fetchListing(basics);

    });
});

function fetchListing(paydata){
    $('#preloader').show();
    $('.card-list').empty();
    var appurl = '/feather/listings/';
    $.ajax({ url: appurl, type: 'GET', data: paydata, dataType: 'json' })
    .done(function(response, textStatus, jqXHR){
        var data = response.data,
        itemlist = data.entity_list,
        item = null;
        $('.h5m').text(data.title.head);
        $('.sp5m').text(data.title.subtitle);

        if (data.total > 0){
            console.log('data.total ', data.total);
            $.each(itemlist, function(index){
                item = itemlist[index];
                var el = "<div class=\"card noborder\">\n" +
                    "        <div class=\"row\" style=\"margin-left: 0;\">\n" +
                    "            <div class=\"col-3of8 p-t-1 card__image\" style=\"background-image: url('"+ item.img +"');\">\n" +
                    "                <img src=\" "+ item.img +"\" alt=\"\" />\n" +
                    "                <span class=\"card__banner\">"+ item.type +"</span>\n" +
                    "            </div>\n" +
                    "            <div class=\"col-5of8 p-x-2\">\n" +
                    "                <span class=\"card__title\"><a href=\"  "+ item.url +"\">"+ item.title +"</a></span>\n" +
                    "                <span class=\"card__price\">"+ item.price +"<i class=\"card__featured fa fa-certificate\"></i></span>\n" +
                    "                <div class=\"card__meta\" style=\"margin-bottom: .35rem;\">\n" +
                    "                    <span class=\"meta__item\">"+ item.location +"</span>\n" +
                    "                    <span class=\"meta__item text-muted\">"+ item.date +"</span>\n" +
                    "                </div>\n" +
                    "                <p class=\"card__text\">"+ item.description +"</p>\n" +
                    "        <!-- div class=\"card__actions\">\n" +
                    "          <button class=\"button\">Check Availability</button>\n" +
                    "        </div -->\n" +
                    "            </div>\n" +
                    "        </div>\n" +
                    "    </div>";
                $(el).appendTo($('.card-list'));
            });
        } else {
            var el = "<div class=\"card noborder\">\n" +
                    "        <div class=\"row\" style=\"margin-left: 0;\">\n" +
                    "            <div class=\"col-8of8 p-x-2\">\n" +
                    "                <span class=\"card__title\">No result found</span>\n" +
                    "                <span class=\"card__price\"></span>\n" +
                    "                <p class=\"card__text\">Unfortunately we found no result for your search. You " +
                    "                   can refine by changing the location and/or the number of bedrooms, you can " +
                    "                   also change the number of bathrooms and then, try again.</p>\n" +
                    "        <!-- div class=\"card__actions\">\n" +
                    "          <button class=\"button\">Check Availability</button>\n" +
                    "        </div -->\n" +
                    "            </div>\n" +
                    "        </div>\n" +
                    "    </div>";
            $(el).appendTo($('.card-list'));
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log('Failed');
    }).always(function(response, textStatus, jqXHR){
        console.log('Done');
        $('#preloader').hide();
        window.scrollTo(0, 0);
    });
}
