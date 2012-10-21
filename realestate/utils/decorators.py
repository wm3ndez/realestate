
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils import simplejson

def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        response = f(request, *args, **kwargs)

        return HttpResponse(
            simplejson.dumps(response),
            content_type='application/javascript',
            status=200,
        )

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

  