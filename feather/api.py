import json
from .utils import get_page_marks, generate_filter_dict, build_sort_args, prepare_model_fields
from .models import Listing

from sorl.thumbnail.shortcuts import get_thumbnail
from django.contrib.humanize.templatetags.humanize import naturaltime
from feather.templatetags.extra_functions import currency


def get_listings(request, resp):
    if hasattr(request, "user") and hasattr(request.user, "userprofile"):
        userprofile = request.user.userprofile

    if request.params:
        data = request.params
        if type(data) is str:
            data = json.loads(data)

        sort_field = data.get('sortField', '-name')
        pg_index = data.get('pageIndex', 1)
        pg_size = data.get('pageSize', 10)
        search_query = data.get('search', None)
        fetch_all = data.get('fetch_all', False)

        title = {
            'head': 'Featured Listings',
            'subtitle': 'List of popular and high demand Listings'
        }

        # Get the page markers
        page_marks = get_page_marks(pg_index, pg_size)

        filter_args = {'active': True}
        if search_query:
            location = data.get('location', None)
            bedroom = int(data.get('bedrooms', 0))
            bathroom = int(data.get('bathrooms', 0))

            if location:
                filter_args['location__name__contains'] = location

            if bedroom and bedroom < 4:
                filter_args['beds__exact'] = bedroom
            elif bedroom and bedroom == 4:
                filter_args['beds__gte'] = bedroom
            else:
                pass

            if bathroom and bathroom < 4:
                filter_args['baths__exact'] = bathroom
            elif bathroom and bathroom == 4:
                filter_args['baths__gte'] = bathroom
            else: pass

            title = {
                'head': 'Search Results',
                'subtitle': 'Response for your search request'
            }
        else:
            filter_args['featured'] = True

        # Generate the filter for the query
        print('filter_args ', filter_args)

        # Prepare the arguments for the query string
        if sort_field:
            args = build_sort_args(sort_field)
            # Query the model for the result
            listings_result_set = Listing.objects.filter(**filter_args).order_by(*args)
        else:
            # Query the model for the result
            listings_result_set = Listing.objects.filter(**filter_args)

        # record size
        total = listings_result_set.count()


        if not fetch_all:
            # Page the result result based on the requested parameters
            listings_result_set = listings_result_set[page_marks['lm']:page_marks['um']]


        entity_list = []
        if listings_result_set:
            for listing in listings_result_set:

                try:
                    im = get_thumbnail(listing.main_image.image, '350x170', crop='center', quality=99).url
                except (ValueError, AttributeError):
                    im = ''

                entity_list.append({
                    'title': listing.title,
                    'description': listing.description,
                    'type': listing.get_type_display(),
                    'date': naturaltime(listing.created_at),
                    'id': listing.id,
                    'url': listing.get_absolute_url(),
                    'location': '%s' % listing.get_address(),
                    'price': currency(listing.price),
                    'img': im,
                })

        resp.passed()
        resp.add_param('message', 'Result found for the query made')
        resp.add_param('entity_list', entity_list)
        resp.add_param('total', total)
        resp.add_param('title', title)
    else:
        resp.no_params()
    return resp

def get_listing(request, resp):
    if request.params:
        pass
    else:
        resp.no_params()
    return resp

def add_listing(request, resp):
    if request.params:
        pass
    else:
        resp.no_params()
    return resp

def delete_listing(request, resp):
    if request.params:
        pass
    else:
        resp.no_params()
    return resp

def search_listings(request, resp):

    if request.params:
        pass
    else:
        resp.no_params()
    return resp
