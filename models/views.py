from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.views import generic
from .models import Locality, Simulation, Calculations
from .forms import SimulationForm 
from django.core import serializers


def index(request):
    return render(request, 'index.html')

def dash(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit = False)
            simulation.locality = Locality.objects.get(id = request.POST['locality'])
            simulation.initial_investment = request.POST['initial_investment']
            simulation.initial_year = request.POST['initial_year']
            simulation.revenue_share_rate = request.POST['revenue_share_rate']
            simulation.project_size = request.POST['project_size']
            simulation.discount_rate = request.POST['discount_rate']
            simulation.save()

            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = Locality.objects.filter(name = simulation.locality)[0].name

            years = [int(simulation.initial_year)]
            assessed_20 = [int(simulation.initial_investment)]
            rs_rate = int(simulation.revenue_share_rate)
            effective_rate = [0.60, 0.50, 0.40, 0.30, 0.20]
            mw = [int(simulation.project_size)]
            interest_rate = int(simulation.discount_rate) *.01
            calc = performCalculations(simulation, years, assessed_20, rs_rate, effective_rate, mw, interest_rate)
            calc.save()
            # calculations = serializers.serialize("python", Calculations.objects.filter(id = calc.id))
            

            #n is the number of years from 2020 to 2050
            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(31)})
    else:
        return HttpResponse('Error please select fill out the model generation form')
# Create your views here.

def request_page(request):
    locality_name = request.POST.get('generateButton')
    return render(request, 'testing.html' , {'county': locality_name})

class IndexView(generic.ListView):
    template_name = 'locality-list.html'
    context_object_name = 'all_locality_list'

    def get_queryset(self):
        return Locality.objects.order_by('name')

class NewSimulationView(CreateView):

    def post(self, request):
        locality_name = request.POST.get('generateButton')
        form_class = SimulationForm() 
        form_class.fields['locality'].initial = Locality.objects.get(name = locality_name).id
        return render(request, 'form.html', {'form' : form_class, 'county': locality_name})



def performCalculations(simulation, years, assessed_20, rs_rate, effective_rate, mw, interest_rate):
    #Run each function & extract table of values
    cas_mt = total_cashflow_mt(years, assessed_20, effective_rate)
    cas_rs = total_cashflow_rs(years, rs_rate, mw, interest_rate)
    tot_mt = total_adj_rev_mt(years, assessed_20, effective_rate, interest_rate)
    tot_mt_sum = sum(tot_mt)
    tot_rs = total_adj_rev_rs(years, rs_rate, mw, interest_rate)
    tot_rs_sum = sum(tot_rs)
    

    calc = Calculations.objects.create(simulation=simulation, cas_mt = cas_mt, cas_rs=cas_rs, tot_mt=tot_mt, tot_rs=tot_rs)
    return calc


'''
Calculations
'''
def effective_rate_ext (effective_rate_list):
    '''
    Takes in schedule of effective rates for county + year of initial build
    Extends list with final effective rate to be available for calculations out to 2050
    '''
    last_rate = effective_rate_list[-1]
    while len(effective_rate_list) <= 32:
        effective_rate_list.append(last_rate)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
M&T functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def lifetime_adj_rev_mt(year, assessed_20, effective_rate_list, interest_rate):
    '''
    :param year: calendar year in which the investment is being made
    :param assessed_20: assessed value of all new solar projects built in locality during particular calendar year
    :param effective_rate_list: schedule of a locality's effective M&T tax rate
    :param interest_rate: rate at which values will be discounted
    :return: total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
    '''
    effective_rate_ext(effective_rate_list)
    rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
    for y in range(0, year - 2019): # fill list with zeros for before project existed
        rev_year_y.append(0)
    for n in range(0, 5):  # tax revenue from first 5 years
        revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100
        year_adj_revenue = revenue / ((1 + interest_rate) ** n)
        rev_year_y.append(year_adj_revenue)
    for n in range(5, 10):  # tax revenue from second 5 years
        revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
        year_adj_revenue = revenue / ((1 + interest_rate) ** n)
        rev_year_y.append(year_adj_revenue)
    for n in range(10, 31):  # tax revenue from end of 10 years through 2050
        revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
        year_adj_revenue = revenue / ((1 + interest_rate) ** n)
        rev_year_y.append(year_adj_revenue)
    return rev_year_y
def total_adj_rev_mt(years, investments_20, outer_effective_rate_list, outer_interest_rate):
    '''
    :param years: list of years in which there is expected to be new investments in solar for a locality
    :param investments_20: list of total assessed values of investments in locality for each year
    :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
    :param outer_interest_rate:  rate at which values will be discounted
    :return: total tax revenue from new solar projects >20MW built in a locality out to 2050
    '''
    total = []  # list to add cashflows from each year to
    for n in range(0, 32):
        # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
        total.append(0)
    for yr in range(0, len(years)):
        # selecting matching pair of year and its corresponding assessed value of new solar >20MW
        year_y = years[yr]
        assessed_year_y = investments_20[yr]
        # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
        year_y_lifetime_cash = lifetime_adj_rev_mt(year_y, assessed_year_y, outer_effective_rate_list,
                                                   outer_interest_rate)
        # calculate year_y_lifetime_rev in 2020 $$$
        for n in range(0, 32):
            y_life_pv = year_y_lifetime_cash[n] / ((1 + outer_interest_rate) ** (year_y - 2020))
            # add value from year y to total
            total[n] = total[n] + y_life_pv
    total.pop(0)
    
    for val in range(0, len(total)): # round final numbers to nearest thousand
        total[val] = round(total[val] / 1000)
    
    return total
def yearly_cashflow_mt(year, assessed_20, effective_rate_list):
    '''
    :param year: calendar year in which the investment is being made
    :param assessed_20: assessed value of all new solar projects >20MW built in locality during particular calendar year
    :param effective_rate_list: schedule of a locality's effective M&T tax rate
    :param interest_rate: rate at which values will be discounted
    :return: list of revenues from solar projects >20MW built in indicated year for 30 years
    '''
    effective_rate_ext(effective_rate_list)
    rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
    for y in range(0, year - 2019): # fill list with zeros for period before project is built
        rev_year_y.append(0)
    for n in range(0, 5):  # tax revenue from first 5 years
        revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100
        rev_year_y.append(revenue)
    for n in range(5, 10):  # tax revenue from second 5 years
        revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
        rev_year_y.append(revenue)
    for n in range(10, 31):  # tax revenue from end of 10 years through 2050
        revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
        rev_year_y.append(revenue)
    return rev_year_y
def total_cashflow_mt(years, investments_20, outer_effective_rate_list):
    '''
    :param years: list of years in which there is expected to be new investments in solar for a locality
    :param investments_20: list of assessed values of solar investments >20MW in locality for each indicated year
    :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
    :param outer_interest_rate: rate at which values will be discounted
    :return: list of yearly tax revenue from solar projects >20MW built in a locality out to 2050
    '''
    total = []  # list for storing annual cashflows
    for n in range(0, 32):
        # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
        total.append(0)
    for yr in range(0, len(years)):
        # selecting matching pair of year and its corresponding assessed value of new solar >20MW
        year_y = years[yr]
        assessed_year_y = investments_20[yr]
        # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
        year_y_lifetime_cash = yearly_cashflow_mt(year_y, assessed_year_y, outer_effective_rate_list
                                                   )
        # calculate year_y_lifetime_rev in 2020 $$$
        for n in range(0, 32):
            y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
            # add value from year y to total
            total[n] = total[n] + y_life_pv
    total.pop(0)
    
    for val in range(0, len(total)): # round final numbers to nearest thousand
        total[val] = round(total[val] / 1000)
    return total
    
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Revenue Share functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def lifetime_adj_rev_rs(rate, megawatts, year, interest_rate):
    '''
    :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
    :param megawatts:
    :param year:
    :param interest_rate:
    :return:
    '''
    rev_year_y = []
    for y in range(0, year - 2019):
        rev_year_y.append(0)
    for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
        revenue = (float(rate * megawatts))
        year_adj_revenue = revenue / ((1 + interest_rate) ** n)
        rev_year_y.append(year_adj_revenue)
    return rev_year_y
def total_adj_rev_rs(years, rate, megawatts, interest_rate):
    '''
    :param years:
    :param rate:
    :param megawatts:
    :param effective_rate_list:
    :param interest_rate:
    :return:
    '''
    total = []  # bin to add present value of lifetime tax revenue from each year to
    for n in range(0, 32):
        # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
        total.append(0)
    for yr in range(0, len(years)):
        # calculate yearly list of cash flows for new builds in year yr
        year_y = years[yr]
        megawatts_y = megawatts[yr]
        year_y_lifetime_cash = lifetime_adj_rev_rs(rate, megawatts_y, year_y, interest_rate)
        # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
        for n in range(0, len(year_y_lifetime_cash)):
            y_life = year_y_lifetime_cash[n] / ((1 + interest_rate) ** (year_y - 2020))
            total[n] = total[n] + y_life
    total.pop(0)
        
    for val in range(0, len(total)): # round final numbers to nearest thousand
        total[val] = round(total[val] / 1000)
    return total
    
    
def lifetime_cashflow_rs(rate, megawatts, year, interest_rate):
    '''
    :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
    :param megawatts: size in MW of all new solar projects >5MW built in locality during particular calendar year
    :param year: calendar year in which the investment is being made
    :param interest_rate:  rate at which values will be discounted
    :return: list of revenues from solar projects >5MW built in indicated year through 2050
    '''
    rev_year_y = []
    for y in range(0, year - 2019):
        rev_year_y.append(0)
    for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
        revenue = (float(rate * megawatts))
        rev_year_y.append(revenue)
    return rev_year_y
def total_cashflow_rs(years, rate, megawatts, interest_rate):
    '''
    :param years: list of years in which there is expected to be new investments in solar for a locality
    :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
    :param megawatts: list of size in MW of total solar investments >5MW in locality for each indicated year 
    :param interest_rate: rate at which values will be discounted
    :return:  list of yearly tax revenue from solar projects >5MW built in a locality out to 2050
    '''
    total = []  # bin to add present value of lifetime tax revenue from each year to
    for n in range(0, 32):
        # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
        total.append(0)
    for yr in range(0, len(years)):
        # calculate yearly list of cash flows for new builds in year yr
        year_y = years[yr]
        megawatts_y = megawatts[yr]
        year_y_lifetime_cash = lifetime_cashflow_rs(rate, megawatts_y, year_y, interest_rate)
        # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
        for n in range(0, len(year_y_lifetime_cash)):
            y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
            total[n] = total[n] + y_life_pv
            
    total.pop(0) # remove 2019 place holder
    
    for val in range(0, len(total)): # round final numbers to nearest thousand
        total[val] = round(total[val] / 1000)
        
    return total
