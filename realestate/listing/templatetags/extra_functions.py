from django.contrib.humanize.templatetags.humanize import intcomma
from django import template
import cgi

register = template.Library()

#register.filter('currency', currency)
@register.filter
def currency(dollars):
    try:
        dollars = float(dollars)
    except ValueError:
        return '$0'
    #return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])
    return "$%s" % intcomma(int(dollars), False)


@register.filter
def get_filename(string):
    return string.split('/')[-1]


#copiado de: http://www.evaisse.net/2008/django-var-dump-print-r-template-tag-17001
@register.tag
def vardump(parser, token):
    tagname, varname = token.contents.split()
    return VardumpRenderer(varname)


class VardumpRenderer(template.Node):
    def __init__(self, var):
        self.var = var


def render(self, context):
    try:
        var = template.resolve_variable(self.var, context)
        t = type(var)
        return cgi.escape("%s => %s" % (t, var))
    except template.VariableDoesNotExist:
        return 'VariableDoesNotExist'