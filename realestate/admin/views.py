from braces.views import StaffuserRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView
from realestate.listing.models import Listing


class Dashboard(TemplateView, StaffuserRequiredMixin):
    template_name = 'admin-panel/dashboard.html'


class CreateListing(CreateView, StaffuserRequiredMixin):
    template_name = 'admin-panel/create-listing.html'
    model = Listing

class Listings(ListView, StaffuserRequiredMixin):
    template_name = 'admin-panel/listings.html'
    model = Listing