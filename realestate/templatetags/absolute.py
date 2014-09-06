# -*- coding: utf-8 -*-
# Taken from https://github.com/noirbizarre/django-absolute

from django.contrib.sites.models import Site
from django.template import Library
from django.template.defaulttags import URLNode, url

register = Library()


class AbsoluteUrlNode(URLNode):
    def render(self, context):
        asvar, self.asvar = self.asvar, None  # Needed to get a return value from super
        path = super(AbsoluteUrlNode, self).render(context)
        self.asvar = asvar
        request = context['request']
        absolute_url = request.build_absolute_uri(path)
        if asvar:
            context[asvar] = absolute_url
            return ''
        else:
            return absolute_url


@register.tag
def absolute(parser, token):
    '''
    Returns a full absolute URL based on the request host.

    This template tag takes exactly the same paramters as url template tag.
    '''
    node = url(parser, token)
    return AbsoluteUrlNode(
        view_name=node.view_name,
        args=node.args,
        kwargs=node.kwargs,
        asvar=node.asvar
    )


class SiteUrlNode(URLNode):
    def render(self, context):
        asvar, self.asvar = self.asvar, None  # Needed to get a return value from super
        path = super(SiteUrlNode, self).render(context)
        self.asvar = asvar
        domain = Site.objects.get_current().domain
        if 'request' in context:
            request = context['request']
            protocol = 'https' if request.is_secure() else 'http'
        else:
            protocol = 'http'
        site_url = "%s://%s%s" % (protocol, domain, path)
        if asvar:
            context[asvar] = site_url
            return ''
        else:
            return site_url


@register.tag
def site(parser, token):
    '''
    Returns a full absolute URL based on the current site.

    This template tag takes exactly the same paramters as url template tag.
    '''
    node = url(parser, token)
    return SiteUrlNode(
        view_name=node.view_name,
        args=node.args,
        kwargs=node.kwargs,
        asvar=node.asvar
    )