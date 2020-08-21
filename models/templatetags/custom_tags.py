from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations

@register.filter
def get_index(l, i):
    return l[i]

@register.simple_tag
def get_totals(l):
    sum = 0
    for item in l:
        sum += item
    return sum