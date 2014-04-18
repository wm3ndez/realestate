from django.conf import settings
from django.core.mail.message import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from realestate.home.forms import SearchForm
from realestate.propiedad.forms import PropiedadContactForm
from realestate.propiedad.models import Propiedad
from realestate.utils import paginate
from realestate.utils.decorators import ajax_required
from sorl.thumbnail.shortcuts import get_thumbnail

if settings.PROPIEDADES_POR_PAGINA:
    PROPIEDADES_POR_PAGINA = settings.PROPIEDADES_POR_PAGINA
else:
    PROPIEDADES_POR_PAGINA = 15


def _render_search_page(queryset, request, template='propiedad/search.html'):
    resultado = paginate(request, queryset, PROPIEDADES_POR_PAGINA)
    return render_to_response(template, {'resultado': resultado},
                              context_instance=RequestContext(request))


def _apply_search_filters(data, properties):
    if data.get('location'):
        properties = properties.filter(Q(sector__nombre__icontains=data.get('location')) |
                                       Q(sector__ciudad__nombre__icontains=data.get('location')) |
                                       Q(sector__ciudad__provincia__icontains=data.get('location')))
    if data.get('precio_max'):
        properties = properties.filter(precio__lte=data.get('precio_max'))
    if data.get('precio_min'):
        properties = properties.filter(precio__gte=data.get('precio_min'))
    if data.get('tipo'):
        properties = properties.filter(tipo=data.get('tipo'))
    if data.get('oferta'):
        properties = properties.filter(oferta=data.get('oferta'))
    return properties


def _venta_alquiler(tipo, request, oferta='venta', template='propiedad/search.html'):
    if oferta == 'venta':
        prop = Propiedad.objects.venta()
    else:
        prop = Propiedad.objects.alquiler()
    if tipo is not None:
        prop = prop.filter(tipo=tipo)
    if request.GET.get('sort') == '-precio':
        prop = prop.order_by('-precio')
    else:
        prop = prop.order_by('precio')

    return _render_search_page(prop, request, template)


def propiedades(request):
    prop = Propiedad.objects.activas().order_by('-id')
    return _render_search_page(prop, request, template='propiedad/listing.html')


def venta(request, tipo=None):
    return _venta_alquiler(tipo, request, template='propiedad/venta.html')


def alquiler(request, tipo=None):
    return _venta_alquiler(tipo, request, 'alquiler', template='propiedad/alquiler.html')


def search(request):
    res = Propiedad.objects.activas()
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
        prop = Propiedad.objects.get(slug=slug)
    except Propiedad.DoesNotExist:
        return HttpResponse("Esta propiedad no existe.")

    if request.POST:
        form = PropiedadContactForm(request.POST)
        if form.is_valid():
            _send_contact_form(form, prop)
            form = PropiedadContactForm()
            #TODO: Redirect to a thank you page
    else:
        form = PropiedadContactForm()

    recentp = Propiedad.objects.all().order_by('-creacion')[:5]
    data = {'propiedad': prop, 'recent': recentp, 'form': form}
    return render_to_response("propiedad/propiedad.html", data, context_instance=RequestContext(request))


@ajax_required
def get_mapa_propiedades(request):
    from realestate.propiedad.templatetags.extra_functions import currency

    listado_propiedades = []
    for propiedad in Propiedad.objects.activas():
        lat, lng = propiedad.coordenadas.split(',')
        try:
            im = get_thumbnail(propiedad.imagen_principal.imagen, '135x90', crop='center', quality=99).url
        except (ValueError, AttributeError):
            im = ''

        try:
            url = propiedad.get_absolute_url()
        except:
            url = ''
        listado_propiedades.append({
            'id': propiedad.id,
            'url': url,
            'street': propiedad.get_address(),
            'title': propiedad.titulo,
            'lat': lat,
            'lng': lng,
            'price': currency(propiedad.precio),
            'img': im,


        })

    return {'propiedades': listado_propiedades, }


def _send_contact_form(form, prop):
    asunto = '%s %s' % ('Cliente Interesado en la propiedad:', prop.titulo)
    mensaje = "El cliente %s esta interesado en esta propiedad y le ha dejado el siguiente mensaje:\n\n%s\n\nTelefono: %s" % (
        form.cleaned_data.get('nombre'), form.cleaned_data.get('mensaje'), form.cleaned_data.get('telefono'))
    _from = settings.DEFAULT_FROM_EMAIL
    to = [prop.agente.user.email, ]
    reply = form.cleaned_data.get('email')
    email = EmailMessage(asunto, mensaje, _from, to, headers={'Reply-To': reply})
    email.send(fail_silently=False)
