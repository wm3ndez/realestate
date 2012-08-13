from django.core.mail import send_mail
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


def _render_search_page(queryset, request):
    queryset = queryset.order_by('-id')
    resultado = _get_paginator(queryset, request)
    return render_to_response("propiedad/search.html", {'resultado': resultado},
        context_instance=RequestContext(request))


def _apply_search_filters(request, properties):
    if request.POST['provincia']:
        properties = properties.filter(sector__ciudad__provincia__icontains=request.POST['provincia'])
    if request.POST['precio_max']:
        properties = properties.filter(precio__lte=request.POST['precio_max'])
    if request.POST['precio_min']:
        properties = properties.filter(precio__gte=request.POST['precio_min'])
    if request.POST['tipo']:
        properties = properties.filter(tipo=request.POST['tipo'])
    if request.POST['oferta']:
        properties = properties.filter(oferta=request.POST['oferta'])
    return properties


def _venta_alquiler(tipo, request, oferta='venta'):
    if oferta == 'venta':
        prop = Propiedad.objects.activas().filter(oferta__exact='venta')
    else:
        prop = Propiedad.objects.activas().filter(oferta__exact='alquiler')
    if tipo is not None:
        prop = prop.filter(tipo=tipo)
    return _render_search_page(prop, request)


def propiedades(request):
    prop = Propiedad.objects.activas().order_by('-id')
    return _render_search_page(prop, request)


def venta(request, tipo=None):
    return _venta_alquiler(tipo, request)


def renta(request, tipo=None):
    return _venta_alquiler(tipo, request, 'alquiler')


def search(request):
    res = Propiedad.objects.activas()
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            res = _apply_search_filters(request, res)

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
    send_mail(asunto, mensaje, form.cleaned_data.get('email'),
        [prop.agente.user.email, ], fail_silently=False)
