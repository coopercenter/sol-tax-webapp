from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations

@register.filter
def get_index(l, i):
    return l[i]

@register.filter
def get_discount_rate(sim):
    print(sim)
    return sim[0]["fields"]["discount_rate"]

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
    # localities = Locality.objects.order_by('name')
    # return {
    #     'all_localities': localities
    # }