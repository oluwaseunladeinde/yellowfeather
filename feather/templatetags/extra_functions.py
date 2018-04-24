from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
from feather.models import Listing, Location

register = template.Library()


@register.filter
def currency(naira):
    try:
        naira = float(naira)
    except (ValueError, TypeError):
        return '₦0'
    return "₦%s" % intcomma(int(naira), False)

@register.inclusion_tag('home/featured.html')
def get_featured(limit=5):
    properties = Listing.objects.featured()[:limit]
    return {'listings': properties}


@register.inclusion_tag('feather/search_widget.html')
def get_search(limit=5):
    locations = Location.objects.all()
    return {'locations': locations}

