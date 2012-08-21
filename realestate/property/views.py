from django.conf import settings
from django.core.mail.message import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from realestate.home.forms import SearchForm
from realestate.property.forms import PropiedadContactForm
from realestate.property.models import  Propiedad
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

PROPIEDADES_POR_PAGINA = 10

def _get_paginator(propiedades, request):
    paginator = Paginator(propiedades, PROPIEDADES_POR_PAGINA)
    page = request.GET.get('page')
    try:
        resultado = paginator.page(page)
    except TypeError:
        # If page is not an integer, deliver first page.
        resultado = paginator.page(1)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        resultado = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        resultado = paginator.page(paginator.num_pages)
    return resultado


def _render_search_page(queryset, request, template='propiedad/search.html'):
    queryset = queryset.order_by('-id')
    resultado = _get_paginator(queryset, request)
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
        prop = Propiedad.objects.activas().filter(oferta__exact='venta')
    else:
        prop = Propiedad.objects.activas().filter(oferta__exact='alquiler')
    if tipo is not None:
        prop = prop.filter(tipo=tipo)
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
    #import ipdb; ipdb.set_trace()
    if request.POST:
        form = SearchForm(request.POST)
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


def _send_contact_form(form, prop):
    asunto = '%s %s' % ('Cliente Interesado en la propiedad:', prop.titulo)
    mensaje = "El cliente %s esta interesado en esta propiedad y le ha dejado el siguiente mensaje:\n\n%s" % (
        form.cleaned_data.get('nombre'), form.cleaned_data.get('mensaje'))
    _from = settings.DEFAULT_FROM_EMAIL
    to = [prop.agente.user.email, ]
    reply = form.cleaned_data.get('email')
    email = EmailMessage(asunto, mensaje, _from, to, headers={'Reply-To': reply})
    email.send(fail_silently=False)