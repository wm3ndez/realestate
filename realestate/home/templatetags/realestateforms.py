from django.template import Library
import ipdb

register = Library()


@register.filter
def widget_with_classes(widget, classes):
    # with ipdb.launch_ipdb_on_exception():
    widget.field.widget.attrs['class'] = classes
    return widget


@register.filter
def widget_with_placeholder(widget, placeholder):
    widget.field.widget.attrs['placeholder'] = placeholder
    return widget