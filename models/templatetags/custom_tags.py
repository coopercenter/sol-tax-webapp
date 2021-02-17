from django import template

register = template.Library()

from ..models import Locality, Simulation, Calculations, UserProfile

#######
# These functions are new tags that can be used in html files
# to get data from variables passed from the views to the templates.
#######

@register.simple_tag
def subtract(a, b):
    a_total = sum(a)
    b_total = sum(b)
    return round((a_total-b_total)*1000, -3)

@register.filter
def get_revenue_index(l, i):
    return ("{:.0f}".format(round(l[i]*1000, -3)))

@register.simple_tag
def get_discount_rate(sim):
    locality = UserProfile.objects.get(id = sim[0]["fields"]["user"])
    return locality.discount_rate

@register.simple_tag
def get_rs_rate(sim):
    locality = UserProfile.objects.get(id = sim[0]["fields"]["user"])
    return locality.revenue_share_rate

@register.simple_tag
def get_mt_rate(sim):
    locality = UserProfile.objects.get(id = sim[0]["fields"]["user"])
    return ("{:.2f}".format(locality.mt_tax_rate))

@register.simple_tag
def get_real_property_rate(sim):
    locality = UserProfile.objects.get(id = sim[0]["fields"]["user"])
    print(locality.real_property_rate)
    return ("{:.2f}".format(locality.real_property_rate))

@register.simple_tag
def get_locality(sim):
    locality = UserProfile.objects.get(id = sim[0]["fields"]["user"])
    return locality.name

@register.simple_tag
def get_totals(l):
    sum = 0
    print(l)
    for item in l:
        sum += item
    print(sum)
    return round(sum*1000, -3)

@register.simple_tag
def get_table_totals(l):
    sum = 0
    for item in l:
        sum += item
    return ("{:.1f}".format(round(sum*1000, -3)))

@register.simple_tag
def change_to_percentage(rate):
    return ("{:.2f}".format(round(rate*100, 4)))

@register.simple_tag
def modulo(num, div):
    return num % div

@register.inclusion_tag("search_bar.html")
def all_localities():
    all_localities = Locality.objects.order_by('name')
    return {'all_localities': all_localities}