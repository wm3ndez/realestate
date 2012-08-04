from django.shortcuts import render_to_response
from django.template import RequestContext
from realestate.property.models import Propiedad
from realestate.home.forms import SearchForm


def index(request):
    recentp = Propiedad.objects.all().order_by('-creacion')[:5]
    form = SearchForm()
    data = {
        'recent': recentp,
        'form': form,
        }
    return render_to_response("index.html", data,
        context_instance=RequestContext(request))


def escribenos(request):
    return render_to_response('home/escribenos.html', {},
        context_instance=RequestContext(request))


def nosotros(request):
    return render_to_response('home/nosotros.html', {},
            context_instance=RequestContext(request))

def contacto(request):
    return render_to_response('home/contacto.html', {},
            context_instance=RequestContext(request))


def servicios(request):
    return render_to_response('home/servicios.html', {},
            context_instance=RequestContext(request))
