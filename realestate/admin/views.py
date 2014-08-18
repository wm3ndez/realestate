from braces.views import StaffuserRequiredMixin, LoginRequiredMixin, OrderableListMixin, SuperuserRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from realestate.home.models import Contact
from realestate.api.models import ApiKeys as ApiKey
from realestate.listing.models import Listing, Agent, Deal, Location
from realestate.admin.forms import ListingForm, ListingImageFormSet, AttributeListingFormSet, ConstanceForm, UserForm, \
    SetPasswordForm

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


class Dashboard(LoginRequiredMixin, StaffuserRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'


class CreateListing(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    template_name = 'dashboard/create-listing.html'
    model = Listing
    form_class = ListingForm
    success_url = reverse_lazy('admin-list-listing')

    def get_context_data(self, **kwargs):
        context = super(CreateListing, self).get_context_data(**kwargs)
        context['states'] = Location.objects.states()
        if self.request.POST:
            context['listing_images_form'] = ListingImageFormSet(self.request.POST, self.request.FILES)
            context['listing_attributes_form'] = AttributeListingFormSet(self.request.POST, self.request.FILES)
        else:
            context['listing_images_form'] = ListingImageFormSet()
            context['listing_attributes_form'] = AttributeListingFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        listing_images_form = context['listing_images_form']
        listing_attributes_form = context['listing_attributes_form']

        if listing_images_form.is_valid() and form.is_valid() and listing_attributes_form.is_valid():
            self.object = form.save()  # saves parent and children
            listing_images_form.instance = self.object
            listing_images_form.save()
            listing_attributes_form.instance = self.object
            listing_attributes_form.save()

            messages.success(self.request, _('Listing created successfully.'))

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class UpdateListing(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    template_name = 'dashboard/create-listing.html'
    model = Listing
    form_class = ListingForm
    success_url = reverse_lazy('admin-list-listing')

    def get_context_data(self, **kwargs):
        context = super(UpdateListing, self).get_context_data(**kwargs)
        if self.request.POST:
            context['listing_images_form'] = ListingImageFormSet(self.request.POST, self.request.FILES,
                                                                 instance=self.object)
            context['listing_attributes_form'] = AttributeListingFormSet(self.request.POST, self.request.FILES,
                                                                         instance=self.object)
        else:
            context['listing_images_form'] = ListingImageFormSet(instance=self.object)
            context['listing_attributes_form'] = AttributeListingFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        listing_images_form = context['listing_images_form']
        listing_attributes_form = context['listing_attributes_form']

        if listing_images_form.is_valid() and form.is_valid() and listing_attributes_form.is_valid():
            form.save()  # saves parent and Children
            listing_images_form.save()
            listing_attributes_form.save()

            messages.success(self.request, _('Listing updated successfully.'))

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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
