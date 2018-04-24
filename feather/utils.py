# -*- coding: utf-8 -*-
import string, re, math
from decimal import Decimal
from django.utils import six
from django.db.models import AutoField


def validation_simple(value, obj=None):
    """
    Validates that at least one character has been entered.
    Not change is made to the value.
    """
    # TODO: Translate
    if value is None or len(value) == 0:
        return False, value, u'El valor digitado debe tener uno o más caracteres'

    return True, value, ''


def validation_integer(value, obj=None):
    """
   Validates that value is an integer number.
   No change is made to the value
    """
    try:
        int(value)
        return True, value, ''
    except:
        # TODO: Translate
        return False, value, u'El valor digitado no es un número entero'


def validation_yesno(value, obj=None):
    """
    Validates that yes or no is entered.
    Converts the yes or no to capitalized version
    """
    if value is not None:
        if six.PY3:
            if str.upper(value) in ["YES", "NO"]:
                return True, str.capitalize(value), ''
        else:
            if string.upper(value) in ["YES", "NO"]:
                return True, string.capitalize(value), ''

    # TODO: Translate
    return False, value, u'El valor digitado debe ser YES o NO'


def validation_decimal(value, obj=None):
    """
    Validates that the number can be converted to a decimal
    """
    try:
        Decimal(value)
        return True, value, ''
    except:
        # TODO: Translate
        return False, value, u'El valor digitado debe ser un número decimal'


def import_validator(validator):
    if validator is None:
        raise ImportError
    try:
        import_name, function_name = validator.rsplit('.', 1)
    except ValueError:
        # no dot; treat it as a global
        func = globals().get(validator, None)
        if not func:
            # we use ImportError to keep error handling for callers simple
            raise ImportError
        return validator
    else:
        # The below __import__() call is from python docs, and is equivalent to:
        #
        # from import_name import function_name
        #
        import_module = __import__(import_name, globals(), locals(), [function_name])

        return getattr(import_module, function_name)


def validate_attribute_value(attribute, value, obj):
    """
    Helper function for forms that wish to validation a value for an
    AttributeOption.
    """
    return import_validator(attribute.validation)(value, obj)


def copy_model_instance(obj):
    """
    Taken from https://djangosnippets.org/snippets/1040/
    """
    initial = dict([
        (f.name, getattr(obj, f.name)) for f in obj._meta.fields if
        not isinstance(f, AutoField) and not f in obj._meta.parents.values()
    ])
    return obj.__class__(**initial)

def get_page_marks(pageIndex, pageSize):
    """

    :param pageIndex:
    :param pageSize:
    :return:
    """
    lower_mark = (int(pageIndex) - 1) * int(pageSize)
    upper_mark = int(pageIndex) * int(pageSize)
    return {'lm': lower_mark, 'um': upper_mark}


def generate_filter_dict(model, filterset=None):
    """
    Used the generate the filter for the query based of the parameters sent from the request.
    :param filterset: A dict of query parameters i.e. key/value
    :return appfilter: A cleaned up (is valid property on model) dict of query parameters
    """
    appfilter = {'active': True, 'featured': True}
    if filterset:
        for key, value in filterset.items():
            field = getattr(model, key, None)
            if field:
                appfilter[key] = value
    return appfilter

def prepare_model_fields(list_fields=None):
    """
    Adds the extra keys needed for the response on the model
    :param list_fields:
    :return fields: Updated list of properties picked from a object to create the response
    """
    # Default fields
    fields = ['slug', 'name', 'description', 'created_at']
    if list_fields:
        fields.extend(list_fields)
    return fields

def build_sort_args(sortFlds):
    """
    Build sort argumenets
    :param sortFlds:
    :return:
    """
    print ("-- There are %s sort fields specified --" % sortFlds)
    args = ()
    flds = str(sortFlds).split(',')
    if len(flds) > 0:
        args = tuple(flds)
    print ("-- Sort Fields --", args)
    return args

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    > normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields
    entry_query = get_query(query_string, ['field1', 'field2', 'field3'])
    found_entries = Model.objects.filter(entry_query).order_by('-something')
    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def nagivation_list(count, per_page, cur_page):
    pagination_nav = ""
    previous_btn = True
    next_btn = True
    first_btn = True
    last_btn = True

    no_of_paginations = int(math.ceil(count / per_page))

    if cur_page >= 7:
        start_loop = cur_page - 3
        if no_of_paginations > cur_page + 3:
            end_loop = cur_page + 3
        elif cur_page <= no_of_paginations and cur_page > no_of_paginations - 6:
            start_loop = no_of_paginations - 6
            end_loop = no_of_paginations
        else:
            end_loop = no_of_paginations
    else:
        start_loop = 1
        if no_of_paginations > 7:
            end_loop = 7
        else:
            end_loop = no_of_paginations

    # Pagination Buttons logic
    pagination_nav += "<div class='pagination-container'><ul>"

    if first_btn and cur_page > 1:
        pagination_nav += "<li p='1' class='active'>First</li>"
    elif first_btn:
        pagination_nav += "<li p='1' class='inactive'>First</li>"

    if previous_btn and cur_page > 1:
        pre = cur_page - 1
        pagination_nav += "<li p='" + str(pre) + "' class='active'>Previous</li>"
    elif previous_btn:
        pagination_nav += "<li class='inactive'>Previous</li>"

    for i in range(start_loop, end_loop + 1):
        if cur_page == i:
            pagination_nav += "<li p='" + str(i) + "' class = 'selected'>" + str(i) + "</li>"
        else:
            pagination_nav += "<li p='" + str(i) + "' class='active'>" + str(i) + "</li>"

    if next_btn and cur_page < no_of_paginations:
        nex = cur_page + 1
        pagination_nav += "<li p='" + str(nex) + "' class='active'>Next</li>"
    elif next_btn:
        pagination_nav += "<li class='inactive'>Next</li>"

    if last_btn and cur_page < no_of_paginations:
        pagination_nav += "<li p='" + str(no_of_paginations) + "' class='active'>Last</li>"
    elif last_btn:
        pagination_nav += "<li p='" + str(no_of_paginations) + "' class='inactive'>Last</li>"

    pagination_nav = pagination_nav + "</ul></div>"

    return pagination_nav
