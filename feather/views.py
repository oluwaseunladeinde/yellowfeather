from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib import auth, messages
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.db.models.query_utils import Q
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateResponseMixin

from braces.views import AjaxResponseMixin, JSONResponseMixin

from .forms import ListingContactForm, FeatherSignupForm
from .models import Listing, Agent, Location
from .api import *
from .constant import *

from core.response import  Response
from rest_framework.reverse import reverse_lazy

from account.views import SignupView, LoginView, LogoutView, ConfirmEmailView
from account.forms import LoginEmailForm
from account.compat import reverse, is_authenticated
from account.models import SignupCode, EmailAddress, EmailConfirmation

from el_pagination.views import AjaxListView


class IndexView(TemplateView):
    #template_name = 'index.html'
    template_name = 'feather/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        recentp = Listing.objects.active().order_by('-created_at')[:settings.RECENTLY_ADDED]
        properties = Listing.objects.featured()[:5]
        context['recent'] = recentp
        context['properties'] = properties
        context['propcount'] = properties.count()
        #context['locations'] = Location.objects.all()
        return context

class Login(View):

    def get(self, request):
        resp = Response()
        login(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")

    def post(self, request):
        resp = Response()
        login(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


class Register(View):

    def get(self, request):
        resp = Response()
        register(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")

    def post(self, request):
        resp = Response()
        register(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


class ListingsView(View):

    def get(self, request):
        resp = Response()
        get_listings(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")

    def post(self, request):
        resp = Response()
        get_listings(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


class ListingDetailView(View):

    def get(self, request):
        resp = Response()
        get_listing(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")

    def post(self, request):
        resp = Response()
        get_listing(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


class ListingCreateView(TemplateView, View):
    #template_name = 'index.html'
    template_name = 'feather/listing_create.html'

    def post(self, request):
        resp = Response()
        get_listing(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('feather:account_login')
        return super(ListingCreateView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListingCreateView, self).get_context_data(**kwargs)
        context['offertypes'] = OFFERS
        context['bedrooms'] = BEDROOMS_RANGE
        context['bathrooms'] = BATHROOMS_RANGE
        context['states'] = NIGERIA_STATES
        context['listing'] = Listing.objects.last()
        #context['locations'] = Location.objects.all()
        return context

class Search(View):

    def get(self, request):
        resp = Response()
        search_listings(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")

    def post(self, request):
        resp = Response()
        search_listings(request, resp)
        return HttpResponse(resp.get_response(), content_type="application/json")


class ListingForSaleList(ListView):
    template_name = 'listing/results.html'
    model = Listing
    paginate_by = settings.PROPERTIES_PER_PAGE

    def get_queryset(self):
        ordering = self.kwargs.get('order_by', 'pk')
        return Listing.objects.sale().order_by(ordering)

    def get_context_data(self, **kwargs):
        ctx = super(ListingForSaleList, self).get_context_data(**kwargs)
        ctx['sort'] = self.kwargs.get('order_by', 'pk')
        return ctx


class ListingForRentList(ListView):
    template_name = 'listing/results.html'
    model = Listing
    paginate_by = settings.PROPERTIES_PER_PAGE

    def get_queryset(self):
        ordering = self.kwargs.get('order_by', 'pk')
        return Listing.objects.rent().order_by(ordering)

    def get_context_data(self, **kwargs):
        ctx = super(ListingForRentList, self).get_context_data(**kwargs)
        ctx['sort'] = self.kwargs.get('order_by', 'pk')
        return ctx


class ListingView(FormMixin, DetailView):
    #template_name = 'listing/listing.html'
    template_name = 'feather/listing_detail.html'
    model = Listing
    form_class = ListingContactForm
    success_url = reverse_lazy('thank-you')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Listing.objects.all()
        return Listing.objects.active()

    def get_context_data(self, **kwargs):
        context = super(ListingView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        context['form'] = self.get_form(form_class)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.send_contact_form(self.object)
        return super(ListingView, self).form_valid(form)


class AgentList(ListView):
    model = Agent
    context_object_name = 'agents'
    template_name = 'listing/agents.html'

    def get_queryset(self):
        return Agent.objects.active()


class AgentListing(ListView):
    model = Listing
    template_name = 'listing/agent-listings.html'
    paginate_by = settings.PROPERTIES_PER_PAGE
    context_object_name = 'results'

    def get_queryset(self):
        return Listing.objects.active(agent=Agent.objects.get(id=self.kwargs.get('agent'))).order_by('-id')





######################## USER ACCOUNT ########
class LoginView(LoginView):
    form_class = LoginEmailForm
    redirect_field_value = "/feather/"


class SignUpView(SignupView):

    form_class = FeatherSignupForm
    redirect_field_value = "/feather/"

    def get_context_data(self, *args, **kwargs):
        context = super(SignUpView, self).get_context_data(*args, **kwargs)
        context['redirect_field_value'] = '/feather/'
        return context

    def after_signup(self, form):
        self.update_profile(form)
        super(SignUpView, self).after_signup(form)

    def update_profile(self, form):
        profile = self.created_user.profile
        profile.save()


class LogoutView(LogoutView):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, *args, **kwargs):
        context = super(LogoutView, self).get_context_data(*args, **kwargs)
        context['redirect_field_value'] = '/feather/'
        return context

class ConfirmEmailView(ConfirmEmailView):
    pass
