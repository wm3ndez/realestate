from django.core.files.storage import default_storage
from braces.views import StaffuserRequiredMixin, LoginRequiredMixin, OrderableListMixin, SuperuserRequiredMixin
from django.contrib.auth.models import User
from formtools.wizard.views import NamedUrlSessionWizardView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib import messages
from realestate.home.models import Contact
from realestate.api.models import ApiKeys as ApiKey
from realestate.listing.models import Listing, Agent, Deal, Location, ListingImage, AttributeListing
from realestate.admin.forms import ListingForm, ListingImageFormSet, AttributeListingFormSet, ConstanceForm, UserForm, \
    SetPasswordForm

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


class Dashboard(LoginRequiredMixin, StaffuserRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'


class CreateListingWizard(LoginRequiredMixin, StaffuserRequiredMixin, NamedUrlSessionWizardView):
    file_storage = default_storage
    form_list = (
        ('listingdata', ListingForm),
        ('images', ListingImageFormSet),
        ('attributes', AttributeListingFormSet),
    )
    TEMPLATES = {
        "listingdata": "dashboard/create-listing-step1.html",
        "images": "dashboard/create-listing-step2.html",
        "attributes": "dashboard/create-listing-step3.html",
    }

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        cleaned_data = self.get_all_cleaned_data()
        images = cleaned_data.pop('formset-images')
        attributes = cleaned_data.pop('formset-attributes')

        with transaction.atomic():
            listing = Listing.objects.create(**cleaned_data)

            for image in images:
                if len(image) > 0:
                    image['listing'] = listing
                    ListingImage.objects.create(**image)

            for attribute in attributes:
                if len(attribute) > 0:
                    attribute['listing'] = listing
                    AttributeListing.objects.create(**attribute)

        return HttpResponseRedirect(reverse_lazy('admin-list-listing'))


class Listings(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    template_name = 'dashboard/listings.html'
    model = Listing
    paginate_by = 15


class Agents(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/agents.html'
    model = Agent
    orderable_columns = ('id', 'name',)
    orderable_columns_default = 'id'


class CreateAgent(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-agent.html'
    model = Agent
    success_url = reverse_lazy('admin-list-agents')


class UpdateAgent(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-agent.html'
    model = Agent
    success_url = reverse_lazy('admin-list-agents')


class Contacts(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/contacts.html'
    model = Contact
    orderable_columns = ('id', 'name',)
    orderable_columns_default = 'id'


class CreateContact(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-contact.html'
    model = Contact
    success_url = reverse_lazy('admin-list-contacts')


class UpdateContact(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-contact.html'
    model = Contact
    success_url = reverse_lazy('admin-list-contacts')


class Locations(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/locations.html'
    model = Location
    orderable_columns = ('id', 'name', 'parent')
    orderable_columns_default = 'id'


class CreateLocation(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-location.html'
    model = Location
    success_url = reverse_lazy('admin-list-sectors')


class UpdateLocation(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-location.html'
    model = Location
    success_url = reverse_lazy('admin-list-sectors')


class Users(LoginRequiredMixin, SuperuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/users.html'
    model = User
    orderable_columns = ('id', 'first_name', 'last_name',)
    orderable_columns_default = 'id'


class CreateUser(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-user.html'
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('set-user-password', args=(self.object.id,))


class UpdateUser(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('admin-list-users')


class Deals(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/deals.html'
    model = Deal
    orderable_columns = ('id', 'first_name', 'last_name',)
    orderable_columns_default = 'id'


class CreateDeal(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-deal.html'
    model = Deal
    success_url = reverse_lazy('admin-list-sale')


class UpdateDeal(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-deal.html'
    model = Deal
    success_url = reverse_lazy('admin-list-sale')


class SetUserPassword(LoginRequiredMixin, SuperuserRequiredMixin, FormView):
    template_name = 'dashboard/password_reset.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('admin-list-users')

    def form_valid(self, form):
        u = User.objects.get(id=self.kwargs['user_id'])
        u.set_password(form.cleaned_data['new_password'])
        u.save()
        return super(SetUserPassword, self).form_valid(form)


class Settings(LoginRequiredMixin, SuperuserRequiredMixin, FormView):
    template_name = 'dashboard/settings.html'
    form_class = ConstanceForm
    success_url = reverse_lazy('dashboard-settings')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class ApiKeys(LoginRequiredMixin, StaffuserRequiredMixin, OrderableListMixin, ListView):
    template_name = 'dashboard/api_keys.html'
    model = ApiKey
    orderable_columns = ('key',)
    orderable_columns_default = 'key'


class CreateApiKey(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-apikey.html'
    model = ApiKey
    success_url = reverse_lazy('admin-api-keys')


class DeleteApiKey(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    template_name = 'dashboard/apikey-confirm-delete.html'
    model = ApiKey
    success_url = reverse_lazy('admin-api-keys')
