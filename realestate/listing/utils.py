# -*- coding: utf-8 -*-
import string
from decimal import Decimal
from django.db.models import AutoField


def validation_simple(value, obj=None):
    """
    Validates that at least one character has been entered.
    Not change is made to the value.
    """
    if len(value) >= 1:
        return True, value, ''
    else:
        # TODO: Translate
        return False, value, u'El valor digitado debe tener uno o más caracteres'


def validation_integer(value, obj=None):
    """
   Validates that value is an integer number.
   No change is made to the value
    """
    try:
        int(value)
        return True, value, ''
    except:
        # TODO: Translate
        return False, value, u'El valor digitado no es un número entero'


def validation_yesno(value, obj=None):
    """
    Validates that yes or no is entered.
    Converts the yes or no to capitalized version
    """
    if string.upper(value) in ["YES", "NO"]:
        return True, string.capitalize(value), ''
    else:
        # TODO: Translate
        return False, value, u'El valor digitado debe ser YES o NO'


def validation_decimal(value, obj=None):
    """
    Validates that the number can be converted to a decimal
    """
    try:
        Decimal(value)
        return True, value, ''
    except:
        # TODO: Translate
        return False, value, u'El valor digitado debe ser un número decimal'


def import_validator(validator):
    try:
        import_name, function_name = validator.rsplit('.', 1)
    except ValueError:
        # no dot; treat it as a global
        func = globals().get(validator, None)
        if not func:
            # we use ImportError to keep error handling for callers simple
            raise ImportError
        return validator
    else:
        # The below __import__() call is from python docs, and is equivalent to:
        #
        # from import_name import function_name
        #
        import_module = __import__(import_name, globals(), locals(), [function_name])

        return getattr(import_module, function_name)


def validate_attribute_value(attribute, value, obj):
    """
    Helper function for forms that wish to validation a value for an
    AttributeOption.
    """
    return import_validator(attribute.validation)(value, obj)


def copy_model_instance(obj):
    """
    Taken from https://djangosnippets.org/snippets/1040/
    """
    initial = dict([
        (f.name, getattr(obj, f.name)) for f in obj._meta.fields if
        not isinstance(f, AutoField) and not f in obj._meta.parents.values()
    ])
    return obj.__class__(**initial)
