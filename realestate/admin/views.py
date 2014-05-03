from braces.views import StaffuserRequiredMixin, LoginRequiredMixin, OrderableListMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from realestate.home.models import Contact
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


class Agents(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/agents.html'
    model = Agent
    orderable_columns = ('id', 'name',)
    orderable_columns_default = 'id'


class CreateAgent(CreateView, LoginRequiredMixin, StaffuserRequiredMixin):
    template_name = 'dashboard/create-agent.html'
    model = Agent
    success_url = reverse_lazy('admin-list-agents')


class Contacts(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/contacts.html'
    model = Contact
    orderable_columns = ('id', 'name',)
    orderable_columns_default = 'id'


class CreateContact(CreateView, LoginRequiredMixin, StaffuserRequiredMixin):
    template_name = 'dashboard/create-contact.html'
    model = Contact
    success_url = reverse_lazy('admin-list-contacts')
