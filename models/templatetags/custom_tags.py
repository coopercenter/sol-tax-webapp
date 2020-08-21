from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations

@register.filter
def get_index(l, i):
    return l[i]