from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.db.models.query_utils import Q
from django.views.generic import ListView, FormView, DetailView, View
from realestate.listing.forms import ListingContactForm, SearchForm
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


class SearchView(ListView):
    template_name = 'listing/search.html'
    paginate_by = config.PROPERTIES_PER_PAGE

    def get_queryset(self):
        queryset = Listing.objects.active()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('location'):
                queryset = queryset.filter(Q(location__icontains=form.cleaned_data.get('location')))

            if form.cleaned_data.get('type'):
                queryset = queryset.filter(type=form.cleaned_data.get('type'))
            if form.cleaned_data.get('offer'):
                queryset = queryset.filter(offer=form.cleaned_data.get('offer'))

        return queryset


class ListingView(DetailView, FormView):
    template_name = 'listing/listing.html'
    model = Listing
    form_class = ListingContactForm
    success_url = reverse_lazy('thank-you')

    def form_valid(self, form):
        form.send_contact_form(self.object)


class MapView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):
        from realestate.listing.templatetags.extra_functions import currency

        listings = []
        for listing in Listing.objects.active():
            lat, lng = listing.coordenadas.split(',')
            try:
                im = get_thumbnail(listing.main_image.imagen, '135x90', crop='center', quality=99).url
            except (ValueError, AttributeError):
                im = ''

            try:
                url = listing.get_absolute_url()
            except:
                url = ''
            listings.append({
                'id': listing.id,
                'url': url,
                'street': listing.get_address(),
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

