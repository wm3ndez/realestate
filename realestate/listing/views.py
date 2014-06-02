from django.conf import settings
from django.core.mail.message import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import ListView, FormView, TemplateView, DetailView
from realestate.listing.forms import ListingContactForm, SearchForm
from realestate.listing.models import Listing, Agent
from realestate.utils import paginate
from realestate.utils.decorators import ajax_required
from rest_framework.reverse import reverse_lazy
from sorl.thumbnail.shortcuts import get_thumbnail
from django.utils.translation import ugettext as _
from constance import config


def _render_search_page(queryset, request, template='listing/search.html'):
    results = paginate(request, queryset, config.PROPERTIES_PER_PAGE)
    return render_to_response(template, {'results': results},
                              context_instance=RequestContext(request))


def _apply_search_filters(data, listings):
    if data.get('location'):
        listings = listings.filter(Q(sector__name__icontains=data.get('location')) |
                                   Q(sector__city__name__icontains=data.get('location')) |
                                   Q(sector__city__province__icontains=data.get('location')))

    if data.get('type'):
        listings = listings.filter(type=data.get('type'))
    if data.get('offer'):
        listings = listings.filter(offer=data.get('offer'))
    return listings


def _sale_rent(type, request, offer='sale', template='listing/search.html'):
    if offer == 'sale':
        listing = Listing.objects.sale()
    else:
        listing = Listing.objects.rent()
    if type is not None:
        listing = listing.filter(type=type)
    if request.GET.get('sort'):
        listing = listing.order_by(request.GET.get('sort'))

    return _render_search_page(listing, request, template)


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
            queryset = _apply_search_filters(form.cleaned_data, queryset)

        return queryset


class ListingView(DetailView, FormView):
    template_name = 'listing/listing.html'
    model = Listing
    form_class = ListingContactForm
    success_url = reverse_lazy('thank-you')

    def form_valid(self, form):
        _send_contact_form(form, self.object)


@ajax_required
def get_map(request):
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

    return {'listings': listings, }


def _send_contact_form(form, prop):
    asunto = '%s %s' % (_('Customer interested in:'), prop.title)
    # TODO: Translate
    mensaje = "El cliente %s esta interesado en esta listing y le ha dejado el siguiente mensaje:\n\n%s\n\nTelefono: %s" % (
        form.cleaned_data.get('nombre'), form.cleaned_data.get('mensaje'), form.cleaned_data.get('phone'))
    _from = settings.DEFAULT_FROM_EMAIL
    to = [prop.agente.user.email, ]
    reply = form.cleaned_data.get('email')
    email = EmailMessage(asunto, mensaje, _from, to, headers={'Reply-To': reply})
    email.send(fail_silently=False)


def agents(request):
    agent_list = Agent.objects.active()
    data = {'agents': agent_list, }
    return render_to_response("listing/agents.html", data, context_instance=RequestContext(request))


def agent_listings(request, agent):
    listing = Listing.objects.active(agent=Agent.objects.get(id=agent)).order_by('-id')
    return _render_search_page(listing, request, template='listing/agent-listings.html')