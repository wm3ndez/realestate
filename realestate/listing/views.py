from django.conf import settings
from django.core.mail.message import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from realestate.home.forms import SearchForm
from realestate.listing.forms import ListingContactForm
from realestate.listing.models import Listing
from realestate.utils import paginate
from realestate.utils.decorators import ajax_required
from sorl.thumbnail.shortcuts import get_thumbnail

if settings.PROPERTIES_PER_PAGE:
    PROPERTIES_PER_PAGE = settings.PROPERTIES_PER_PAGE
else:
    PROPERTIES_PER_PAGE = 15


def _render_search_page(queryset, request, template='listing/search.html'):
    resultado = paginate(request, queryset, PROPERTIES_PER_PAGE)
    return render_to_response(template, {'resultado': resultado},
                              context_instance=RequestContext(request))


def _apply_search_filters(data, listings):
    if data.get('location'):
        listings = listings.filter(Q(sector__nombre__icontains=data.get('location')) |
                                       Q(sector__ciudad__nombre__icontains=data.get('location')) |
                                       Q(sector__ciudad__provincia__icontains=data.get('location')))
    if data.get('precio_max'):
        listings = listings.filter(precio__lte=data.get('precio_max'))
    if data.get('precio_min'):
        listings = listings.filter(precio__gte=data.get('precio_min'))
    if data.get('type'):
        listings = listings.filter(tipo=data.get('type'))
    if data.get('offer'):
        listings = listings.filter(oferta=data.get('offer'))
    return listings


def _venta_alquiler(tipo, request, oferta='venta', template='listing/search.html'):
    if oferta == 'venta':
        listing = Listing.objects.sale()
    else:
        listing = Listing.objects.rent()
    if tipo is not None:
        listing = listing.filter(tipo=tipo)
    if request.GET.get('sort') == '-price':
        listing = listing.order_by('-price')
    else:
        listing = listing.order_by('price')

    return _render_search_page(listing, request, template)


def properties(request):
    listing = Listing.objects.active().order_by('-id')
    return _render_search_page(listing, request, template='listing/listing.html')


def sale(request, tipo=None):
    return _venta_alquiler(tipo, request, template='listing/venta.html')


def rent(request, tipo=None):
    return _venta_alquiler(tipo, request, 'alquiler', template='listing/alquiler.html')


def search(request):
    res = Listing.objects.active()
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            res = _apply_search_filters(form.cleaned_data, res)
    else:
        form = SearchForm(request.GET)
        if form.is_valid():
            res = _apply_search_filters(form.cleaned_data, res)

    return _render_search_page(res, request)


def details(request, slug):
    try:
        listing = Listing.objects.get(slug=slug)
    except Listing.DoesNotExist:
        return HttpResponse("Esta listing no existe.")

    if request.POST:
        form = ListingContactForm(request.POST)
        if form.is_valid():
            _send_contact_form(form, listing)
            form = ListingContactForm()
            #TODO: Redirect to a thank you page
    else:
        form = ListingContactForm()

    recentp = Listing.objects.all().order_by('-created_at')[:5]
    data = {'listing': listing, 'recent': recentp, 'form': form}
    return render_to_response("listing/propiedad.html", data, context_instance=RequestContext(request))


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
    asunto = '%s %s' % ('Cliente Interesado en la listing:', prop.titulo)
    mensaje = "El cliente %s esta interesado en esta listing y le ha dejado el siguiente mensaje:\n\n%s\n\nTelefono: %s" % (
        form.cleaned_data.get('nombre'), form.cleaned_data.get('mensaje'), form.cleaned_data.get('phone'))
    _from = settings.DEFAULT_FROM_EMAIL
    to = [prop.agente.user.email, ]
    reply = form.cleaned_data.get('email')
    email = EmailMessage(asunto, mensaje, _from, to, headers={'Reply-To': reply})
    email.send(fail_silently=False)
