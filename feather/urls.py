from django.conf.urls import url, include
from .views import *
from .sitemap import ListingSitemap

app_name = 'feather'
urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^listings/$', ListingsView.as_view(), name='all_listings'),
    url(r'^search/listings/$', ListingsView.as_view(), name='search_listings'),
    url(r'^create/listings/$', ListingCreateView.as_view(), name='create_listings'),

    url(r'^sale/$', ListingForSaleList.as_view(), name='properties_for_sale'),
    url(r'^rent/$', ListingForRentList.as_view(), name='properties_for_rent'),
    
    # Account Management
    url(r'^account/signup/$', SignUpView.as_view(), name="account_sign_up"),
    url(r'^account/login/$', LoginView.as_view(), name="account_login"),
    url(r"^account/confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^account/logout/$", LogoutView.as_view(), name="account_logout"),
]
