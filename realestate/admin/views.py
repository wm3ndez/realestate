from braces.views import StaffuserRequiredMixin, LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from realestate.listing.models import Listing, Agent
from realestate.admin.forms import ListingForm


class Dashboard(TemplateView, StaffuserRequiredMixin):
    template_name = 'dashboard/dashboard.html'


class CreateListing(CreateView, StaffuserRequiredMixin):
    template_name = 'dashboard/create-listing.html'
    model = Listing
    form_class = ListingForm


class Listings(ListView, StaffuserRequiredMixin):
    template_name = 'dashboard/listings.html'
    model = Listing