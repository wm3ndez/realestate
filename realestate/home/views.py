from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView
from realestate.listing.models import Listing
from realestate.home.forms import SearchForm
from realestate.home.forms import ContactForm


def index(request):
    recentp = Listing.objects.all().order_by('-created_at')[:5]
    form = SearchForm()
    data = {
        'recent': recentp,
        'form': form,
    }
    return render_to_response("index.html", data, context_instance=RequestContext(request))


class ContactView(FormView):
    template_name = 'home/contact-us.html'
    form_class = ContactForm
    success_url = reverse_lazy('thank-you')


    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)
