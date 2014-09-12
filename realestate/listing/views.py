from django.views.generic.edit import FormMixin
from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.db.models.query_utils import Q
from django.views.generic import ListView, DetailView, View
from realestate.listing.forms import ListingContactForm
from realestate.listing.models import Listing, Agent
from rest_framework.reverse import reverse_lazy
from sorl.thumbnail.shortcuts import get_thumbnail
from constance import config


class ListingList(ListView):
    template_name = 'listing/results.html'
    model = Listing
    queryset = Listing.objects.active()
    paginate_by = config.PROPERTIES_PER_PAGE


class ListingForSaleList(ListView):
    template_name = 'listing/results.html'
    model = Listing
    paginate_by = config.PROPERTIES_PER_PAGE

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
    paginate_by = config.PROPERTIES_PER_PAGE

    def get_queryset(self):
        ordering = self.kwargs.get('order_by', 'pk')
        return Listing.objects.rent().order_by(ordering)

    def get_context_data(self, **kwargs):
        ctx = super(ListingForRentList, self).get_context_data(**kwargs)
        ctx['sort'] = self.kwargs.get('order_by', 'pk')
        return ctx


class ListingView(FormMixin, DetailView):
    template_name = 'listing/listing.html'
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


class MapView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        from realestate.listing.templatetags.extra_functions import currency

        listings = []
        for listing in Listing.objects.active():
            lat, lng = listing.coords.split(',')
            try:
                im = get_thumbnail(listing.main_image.imagen, '135x90', crop='center', quality=99).url
            except (ValueError, AttributeError):
                im = ''

            listings.append({
                'id': listing.id,
                'url': listing.get_absolute_url(),
                'street': '%s' % listing.get_address(),
                'title': listing.title,
                'lat': lat,
                'lng': lng,
                'price': currency(listing.price),
                'img': im,


            })

        return self.render_json_response({'listings': listings, })


class AgentList(ListView):
    model = Agent
    context_object_name = 'agents'
    template_name = 'listing/agents.html'

    def get_queryset(self):
        return Agent.objects.active()


class AgentListing(ListView):
    model = Listing
    template_name = 'listing/agent-listings.html'
    paginate_by = config.PROPERTIES_PER_PAGE
    context_object_name = 'results'

    def get_queryset(self):
        return Listing.objects.active(agent=Agent.objects.get(id=self.kwargs.get('agent'))).order_by('-id')

