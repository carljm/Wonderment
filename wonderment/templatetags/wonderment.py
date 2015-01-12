from django.template import Library

from wonderment.models import today


register = Library()


@register.filter
def age(child):
    return child.age_display(today())
