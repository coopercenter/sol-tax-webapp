from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations

@register.filter
def get_index(l, i):
    return l[i]

@register.filter
def get_revenue_index(l, i):
    return ("{:.1f}".format(l[i]))

@register.simple_tag
def get_discount_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.discount_rate

@register.simple_tag
def get_rs_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.revenue_share_rate

@register.simple_tag
def get_mt_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.mt_tax_rate

@register.simple_tag
def get_real_property_rate(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.real_property_rate

@register.simple_tag
def get_locality(sim):
    locality = Locality.objects.get(id = sim[0]["fields"]["locality"])
    return locality.name

@register.simple_tag
def get_totals(l):
    sum = 0
    # print(l)
    for item in l:
        sum += item
    return round(sum*1000, -3)

@register.inclusion_tag("search_bar.html")
def all_localities():
    all_localities = Locality.objects.order_by('name')
    return {'all_localities': all_localities}