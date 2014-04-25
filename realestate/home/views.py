from django.shortcuts import render_to_response
from django.template import RequestContext
from realestate.listing.models import Listing
from realestate.home.forms import SearchForm


def index(request):
    recentp = Listing.objects.all().order_by('-created_at')[:5]
    form = SearchForm()
    data = {
        'recent': recentp,
        'form': form,
    }
    return render_to_response("index.html", data,
                              context_instance=RequestContext(request))
