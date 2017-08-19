import json as stdlib_json

from django.template import Library

from wonderment.models import today

register = Library()


@register.filter
def age(child):
    return child.age_display(today())


@register.filter
def json(val):
    return stdlib_json.dumps(val)


@register.filter
def newlineslash(val):
    return val.strip().replace('\n', ' / ')


@register.filter
def sign_in_status(child):
    return child.sign_in_status(today())
