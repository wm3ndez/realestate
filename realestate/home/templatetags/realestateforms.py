from django.template import Library

register = Library()


@register.filter
def widget_with_classes(widget, classes):
    widget.field.widget.attrs['class'] = classes
    return widget


@register.filter
def widget_with_placeholder(widget, placeholder):
    widget.field.widget.attrs['placeholder'] = placeholder
    return widget


@register.filter
def widget_attrs(widget, attrs):
    attr_name, attr_value = attrs.split(':')
    widget.field.widget.attrs[attr_name] = ' ' + attr_value
    return widget