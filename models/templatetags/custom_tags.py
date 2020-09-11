from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations

@register.filter
def get_index(l, i):
    return l[i]

@register.simple_tag
def get_discount_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.discount_rate

@register.simple_tag
def get_rs_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.revenue_share_rate

@register.simple_tag
def get_locality(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.name

@register.simple_tag
def get_totals(l):
    sum = 0
    for item in l:
        sum += item
    return "{:,}".format(sum*1000)

@register.inclusion_tag("search_bar.html")
def all_localities():
    all_localities = Locality.objects.order_by('name')
    return {'all_localities': all_localities}