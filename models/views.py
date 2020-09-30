from matplotlib import pylab
from pylab import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.views import generic
from .models import Locality, Simulation, Calculations
from .forms import SimulationForm 
from django.core import serializers
import urllib, base64
import PIL, PIL.Image, io
from django.db.models import Count
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from plotly.offline import plot
import plotly.graph_objects as go

# Landing Page
def index(request):
    return render(request, 'index.html')

# Login Page
def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # Form submitted
            user = form.get_user()
            login(request, user) # Check Login Information
            return HttpResponseRedirect('/locality-' + str(user)+'/') #redirect to locality's home page
        else: # Displays Login Form
            form = AuthenticationForm(initial={'username': request.POST.get('locality')})
    return render(request, 'login.html', {'form': form})

# Logout, redirects to landing page
def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

def localityName(request):
    print(request.GET)
    if(request.POST.get('locality')):
        locality = (request.POST.get('locality'))
    return HttpResponseRedirect('/locality-'+locality+'/')

def profile(request):
    return render(request, 'profile.html')

def locality_home(request, locality_name):
    print(request.POST)
    if request.POST.get('simulation_id'):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        simulation.delete()

    locality = Locality.objects.get(name = locality_name.capitalize())
    if request.POST.get('discount_rate'):
        locality.discount_rate = request.POST.get('discount_rate')
        locality.revenue_share_rate = request.POST.get('revenue_share_rate')
        locality.save()
        for simulation in locality.simulation_set.all():
            values = getSimulationValues(simulation)
            calc = performCalculations(simulation, values[0], values[1], values[2], values[3], values[4], values[5])
            calc.save()

    simulations = locality.simulation_set.all()
    return render(request, 'locality-home.html', {'locality': locality, 'simulations':simulations})


# Creates Scatter Plot using plotly
def scatter(mt, rs):
    x1 = [i for i in range(2020, 2051)]
    y1 = mt
    y2 = rs

    trace = go.Scatter(
        x= x1,
        y = y1,
        name = "M&T Tax"
    )
    trace2 = go.Scatter(
        x = x1,
        y = y2,
        name = "Revenue Share"
    )
    layout = dict(
        xaxis=dict(range=[min(x1), max(x1)], title="Year"),
        yaxis = dict(range=[0, max(max(y1), max(y2))+20], title="Revenue ($ in Thousands)"),
        margin={'t' : 20, 'l':0},
    )

    fig = go.Figure(data=[trace, trace2], layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

def dash(request, locality_name, simulation_id):
    if(request.POST.get('simulation_id')):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
        loc = Locality.objects.filter(name = simulation.locality)[0]
        values = getSimulationValues(simulation)
        print(values)
        initial_year = values[0]
        initial_investment = values[1]
        revenue_share_rate = values[2]
        project_size = values[3]
        discount_rate = values[4]
        effective_rate = values[5]
        project_land = values[6]
        inside_fence_land = values[7]
        baseline_land_value = values[8]
        inside_fence_land_value = values[9]

        #calc = performCalculations(loc, simulation, initial_year, initial_investment, revenue_share_rate, project_size, discount_rate, effective_rate, project_land, inside_fence_land, baseline_land_value, inside_fence_land_value)
        calc = performCalculations(loc, simulation)
        calc.save()

        context = {
            'plot1': scatter(calc.cas_mt, calc.cas_rs)
        }

        return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(31), "graph":context})
    if request.method == 'POST':
        print("post")
        form = SimulationForm(request.POST)
        if form.is_valid():
            print("form")
            simulation = form.save(commit = False)
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = Locality.objects.filter(name = simulation.locality)[0]
            values = getSimulationValues(simulation)
            print(simulation.id)
            initial_year = values[0]
            initial_investment = values[1]
            revenue_share_rate = values[2]
            project_size = values[3]
            discount_rate = values[4]
            effective_rate = values[5]
            project_land = values[6]
            inside_fence_land = values[7]
            baseline_land_value = values[8]
            inside_fence_land_value = values[9]
        
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs)
            }
            # print(sim)
            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(31), "graph":context})
        
        else:
            simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = Locality.objects.filter(name = simulation.locality)[0]
            values = getSimulationValues(simulation)
            print(values)
            initial_year = values[0]
            initial_investment = values[1]
            revenue_share_rate = values[2]
            project_size = values[3]
            discount_rate = values[4]
            effective_rate = values[5]
            project_land = values[6]
            inside_fence_land = values[7]
            baseline_land_value = values[8]
            inside_fence_land_value = values[9]
            
            #calc = performCalculations(loc, simulation, initial_year, initial_investment, revenue_share_rate, project_size, discount_rate, effective_rate, project_land, inside_fence_land, baseline_land_value, inside_fence_land_value)
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs)
            }

            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(31), "graph":context})
    else:
        return HttpResponse('Error please select fill out the model generation form')
# Create your views here.

def request_page(request):
    locality_name = request.POST.get('generateButton')
    return render(request, 'testing.html' , {'county': locality_name})


def index_page(request):
    localities = Locality.objects.order_by('name')
    simulations = Locality.objects.annotate(number_of_simulations=Count('simulation'))
    return render(request, 'locality-list.html', {'localities': localities, 'simulations':simulations})

class NewSimulationView(CreateView):

    def post(self, request):
        if(request.POST.get('viewButton') == None):
            locality_name = request.POST.get('generateButton')
            form_class = SimulationForm() 
            form_class.fields['locality'].initial = Locality.objects.get(name = locality_name).id
            return render(request, 'form.html', {'form' : form_class, 'county': locality_name})
        else:
            return HttpResponseRedirect('/' + request.POST.get('viewButton'))

def getSimulationValues(simulation):
    years = int(simulation.initial_year)
    assessed_20 = int(simulation.initial_investment)
    rs_rate = int(simulation.locality.revenue_share_rate)
    mw = int(simulation.project_size)
    interest_rate = int(simulation.locality.discount_rate) *.01
    property_rate = simulation.locality.real_propery_rate
    mt_rate = simulation.locality.mt_tax_rate
    scc_depreciation = [.9, .9, .9, .9, .9, .87, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10]
    project_land = int(simulation.total_acerage)
    inside_fence_land = int(simulation.inside_fence_acerage)
    baseline_land_value = int(simulation.baseline_land_value)
    inside_fence_land_value = int(simulation.inside_fence_land_value)
    
    # total_acerage = 2354
    # inside_acerage = 910
    # outside_acerage = total_acerage - inside_acerage
    # baseline_value = 1277.16
    # inside_fence_value = 10000
    # outside_fence_value = 1277
    # fmv_increase = 1.2
    # yrs_between = 5


    offset = years - 2020
    effective_rate = []
    for i in range(0, offset):
        effective_rate.append(0)
    
    for i in range(0, 2050 - years + 1):
        if(mw >= 20):
            offset = years-2020
            effective_rate.append(scc_depreciation[i] * property_rate)
        else:
            effective_rate = mt_rate

    return years, assessed_20, rs_rate, mw, interest_rate, effective_rate, project_land, inside_fence_land, baseline_land_value, inside_fence_land_value

def performCalculations(locality, simulation):
    #Run each function & extract table of values
    # print(years, assessed_20, rs_rate, mw, interest_rate, effective_rate)
    # cas_mt = total_cashflow_mt(years, assessed_20, effective_rate)
    # print(cas_mt)
    # cas_rs = total_cashflow_rs(years, rs_rate, mw, interest_rate)
    # tot_mt = total_adj_rev_mt(years, assessed_20, effective_rate, interest_rate)
    # tot_mt_sum = sum(tot_mt)
    # tot_rs = total_adj_rev_rs(years, rs_rate, mw, interest_rate)
    # tot_rs_sum = sum(tot_rs)

    '''
    State Variables
    '''
    state_true_value = [1170092111098.94 for i in range(31)]
    state_adj_gross_income = 269067675604.708
    state_taxable_retail_sales = 100207273998.18
    state_adm = 1239781.3
    state_population = 8382993

    '''
    Locality Variables
    '''
    discount_rate = locality.discount_rate
    revenue_share_rate = locality.revenue_share_rate
    mt_tax_rate = locality.mt_tax_rate
    real_propery_rate = locality.real_propery_rate
    assesment_ratio = locality.assesment_ratio
    local_baseline_true_value = locality.baseline_true_value
    local_adj_gross_income = locality.adj_gross_income
    local_taxable_retail_sales = locality.taxable_retail_sales
    local_population = locality.population
    local_adm = locality.adm
    required_local_matching = locality.required_local_matching
    budget_escalator = locality.budget_escalator


    '''
    Simulation Variables
    '''

    local_investment = simulation.initial_investment
    initial_year = simulation.initial_year
    project_size = simulation.project_size
    total_project_acerage = simulation.total_acerage
    inside_fence_acerage =simulation.inside_fence_acerage
    baseline_land_value = simulation.baseline_land_value
    inside_fence_land_value = simulation.inside_fence_land_value

    # #Revenue Share Works
    cas_rs = total_cashflow_rs(rs_rate, mw, initial_year)
    tot_rs = total_adj_rev(cas_rs, interest_rate)
    tot_rs_sum = int(sum(tot_rs))

    #Revenue Share with Land Works
    cas_mt = total_cashflow_mt(initial_year, investment, effective_rate)
    # cas_mt_land = add_land(cas_mt, land_difference, land_baseline, property_rate)
    # print(cas_mt_land)
    tot_mt = total_adj_rev(cas_mt, interest_rate)
    tot_mt_sum = int(sum(tot_mt))
    # print(tot_rs_sum, tot_mt_sum)

    try:
        sim = simulation.calculations
        calc = Calculations.objects.get(simulation=simulation)
        calc.cas_mt = cas_mt
        calc.cas_rs = cas_rs
        calc.tot_mt = tot_mt
        calc.tot_rs = tot_rs
    except Calculations.DoesNotExist:
        calc = Calculations.objects.create(simulation=simulation, cas_mt = cas_mt, cas_rs=cas_rs, tot_mt=tot_mt, tot_rs=tot_rs)
    return calc


# def land_value(baseline_value, inside_fence_value, outside_fence_value_, fmv_increase, yrs, total_acerage, inside_acerage, outside_acerage):
#     baseline=[]
#     for i in range(31):
#         baseline.append(baseline_value * total_acerage)
#     return baseline



def total_cashflow_mt(year, assessed_20, effective_rate_list):
    '''
        :year: Starting year of solar project
        :assessed_20: Initial investment into solar project
        :effective_rate_list: List of effective rates of m&t over the course of a 30 year period
        :return: list of M&T tax revenue generated each year from 2020-2050, nominal $
    '''
    effective_rate_ext(effective_rate_list)
    # print(assessed_20)
    print(effective_rate_list)
    yearly_rev_mt = []
    for i in range(0, 31):
        if(i + 2020 >= year):
            if i+2020 - year < 5:
                revenue = ((assessed_20 * .2 * effective_rate_list[i])/100)/1000
                yearly_rev_mt.append(revenue)
            elif (i + 2020 - year) >= 5 and (i + 2020 - year) < 10:
                revenue = ((assessed_20 * .3 * effective_rate_list[i])/100)/1000
                yearly_rev_mt.append(revenue)
            elif (i + 2020 - year) >= 10:
                revenue = ((assessed_20 * .4 * effective_rate_list[i])/100)/1000
                yearly_rev_mt.append(revenue)
        else:
            yearly_rev_mt.append(0)
    return yearly_rev_mt

def total_cashflow_rs(revenue_share_rate, megawatts, year):
    '''
        :revenue_share_rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
        :megawatts: Size of solar project
        :year: Starting year of the solar project
        :return: A list of reveneue share revenue generated during each year from 2020-2050, nominal $
    '''
    cashflow_rev = []
    for i in range(0, 31):
        if(i + 2020 >= year):
            cashflow_rev.append((revenue_share_rate * megawatts)/1000) # If the index is at or past the initial year of project
        else:
            cashflow_rev.append(0) #If the index is before the initial year of project
    return cashflow_rev


def total_adj_rev(cas, discount_rate):
    '''
        :cas_rs: List of revenue generate during each year from 2020-2050, nominal $
        :discount_rate: rate at which revenue values will be discounted
        :return: A list of revenue generated during each year from 2020-2050, 2020 $
    '''
    tot_rs = []
    for i in range(len(cas)):
        tot_rs.append(cas[i] / ((1 + discount_rate)**(i + 1))) # Present value formula
    return tot_rs

def land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, starting_year):
    baseline=[]
    inside = []
    outside = []
    difference = []

    offset = starting_year - 2020
    for i in range(0, offset):
        baseline.append(0)
        inside.append(0)
        outside.append(0)


    for i in range(0, 2050-starting_year+1):
        if( i % 5 == 0):
            baseline.append(int(baseline_value * total_acerage * ((1.012)**(i+1))))
        else:
            baseline.append(baseline[i + offset-1])
        if( i % 6 == 0):
            inside.append(int(inside_fence_value * inside_acerage * ((1.012)**(i+1))))
            outside.append(int(outside_fence_value * outside_acerage * ((1.012)**(i+1))))
        else:
            inside.append(inside[i + offset-1])
            outside.append(outside[i + offset-1])
    
    for i in range(len(baseline)):
        difference.append(inside[i] + outside[i] - baseline[i])
    return difference, baseline

# def add_land(cas_mt, land_difference, land_baseline, property_rate):
#     # print("Difference in land values " + str(land_difference))
#     # print("M&T with no Land " + str(cas_mt))
#     cas_mt_land = []
#     for i in range(len(cas_mt)):
#         land_value_by_year = int((land_difference[i]/100 * property_rate)) + int((land_baseline[i]/100 * property_rate))
#         cas_mt_land.append(cas_mt[i] + land_value_by_year)
#     return cas_mt_land

# total_acerage = 2354
# inside_acerage = 910
# outside_acerage = total_acerage - inside_acerage
# baseline_value = 1277.16
# inside_fence_value = 10000
# outside_fence_value = 1277
# fmv_increase = 1.2
# yrs_between = 5

# initial_year = 2020
# investment = 140000000
# rs_rate = 1400
# mt_rate = [0.63]
# property_rate = 0.5
# mw = 100
# interest_rate = 0.06
# scc_depreciation = [.9, .9, .9, .9, .9, .87, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10]

# if(mw >= 20):
#     effective_rate = []
#     for i in range(len(scc_depreciation)):
#         effective_rate.append(scc_depreciation[i] * property_rate)
#     # effective_rate = [property_rate]
# else:
#     effective_rate = mt_rate

# land_values = land_value(total_acerage, inside_acerage, outside_acerage, baseline_value, inside_fence_value, outside_fence_value, fmv_increase, yrs_between, 2020)
# land_difference = land_values[0]
# land_baseline = land_values[1]




# #Revenue Share Works
# cas_rs = total_cashflow_rs(rs_rate, mw, initial_year)
# tot_rs = total_adj_rev(cas_rs, interest_rate)
# tot_rs_sum = int(sum(tot_rs))

# #Revenue Share with Land Works
# cas_mt = total_cashflow_mt(initial_year, investment, effective_rate)
# cas_mt_land = add_land(cas_mt, land_difference, land_baseline, property_rate)
# print(cas_mt_land)
# tot_mt = total_adj_rev(cas_mt_land, interest_rate)
# tot_mt_sum = int(sum(tot_mt))
# print(tot_rs_sum, tot_mt_sum)



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
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# M&T functions
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# def lifetime_adj_rev_mt(year, assessed_20, effective_rate_list, interest_rate):
#     '''
#     :param year: calendar year in which the investment is being made
#     :param assessed_20: assessed value of all new solar projects built in locality during particular calendar year
#     :param effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param interest_rate: rate at which values will be discounted
#     :return: total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#     '''
#     effective_rate_ext(effective_rate_list)
#     rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
#     for y in range(0, year - 2019): # fill list with zeros for before project existed
#         rev_year_y.append(0)
#     for n in range(0, 5):  # tax revenue from first 5 years
#         revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100 # (Project value * Taxable percentage * M&T tax rate) / 100 = M&T revenue Divide by 100 as M&T is calculated per 100 valuation.
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n) 
#         rev_year_y.append(year_adj_revenue)
#     for n in range(5, 10):  # tax revenue from second 5 years
#         revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     for n in range(10, 31):  # tax revenue from end of 10 years through 2050
#         revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     return rev_year_y
# def total_adj_rev_mt(years, investments_20, outer_effective_rate_list, outer_interest_rate):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param investments_20: list of total assessed values of investments in locality for each year
#     :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param outer_interest_rate:  rate at which values will be discounted
#     :return: total tax revenue from new solar projects >20MW built in a locality out to 2050
#     '''
#     total = []  # list to add cashflows from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # selecting matching pair of year and its corresponding assessed value of new solar >20MW
#         year_y = years[yr]
#         assessed_year_y = investments_20[yr]
#         # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#         year_y_lifetime_cash = lifetime_adj_rev_mt(year_y, assessed_year_y, outer_effective_rate_list,
#                                                    outer_interest_rate)
#         # calculate year_y_lifetime_rev in 2020 $$$
#         for n in range(0, 32):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + outer_interest_rate) ** (year_y - 2020))
#             # add value from year y to total
#             total[n] = total[n] + y_life_pv
#     total.pop(0)
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
    
#     return total
# def yearly_cashflow_mt(year, assessed_20, effective_rate_list):
#     '''
#     :param year: calendar year in which the investment is being made
#     :param assessed_20: assessed value of all new solar projects >20MW built in locality during particular calendar year
#     :param effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param interest_rate: rate at which values will be discounted
#     :return: list of revenues from solar projects >20MW built in indicated year for 30 years
#     '''
#     effective_rate_ext(effective_rate_list)
#     rev_year_y = [] # start a list to fill with lifetime cashflows from projects built in year year
#     for y in range(0, year - 2019): # fill list with zeros for period before project is built
#         rev_year_y.append(0)
#     for n in range(0, 5):  # tax revenue from first 5 years
#         revenue = (assessed_20 * .2 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     for n in range(5, 10):  # tax revenue from second 5 years
#         revenue = (assessed_20 * .3 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     for n in range(10, 31):  # tax revenue from end of 10 years through 2050
#         revenue = (assessed_20 * .4 * effective_rate_list[n]) / 100
#         rev_year_y.append(revenue)
#     return rev_year_y
# def total_cashflow_mt(years, investments_20, outer_effective_rate_list):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param investments_20: list of assessed values of solar investments >20MW in locality for each indicated year
#     :param outer_effective_rate_list: schedule of a locality's effective M&T tax rate
#     :param outer_interest_rate: rate at which values will be discounted
#     :return: list of yearly tax revenue from solar projects >20MW built in a locality out to 2050
#     '''
#     total = []  # list for storing annual cashflows
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # selecting matching pair of year and its corresponding assessed value of new solar >20MW
#         year_y = years[yr]
#         assessed_year_y = investments_20[yr]
#         # calculate total lifetime tax revenue from new builds in year y under M&T tax, in year y dollars
#         year_y_lifetime_cash = yearly_cashflow_mt(year_y, assessed_year_y, outer_effective_rate_list
#                                                    )
#         # calculate year_y_lifetime_rev in 2020 $$$
#         for n in range(0, 32):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
#             # add value from year y to total
#             total[n] = total[n] + y_life_pv
#     total.pop(0)
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
#     return total
    









# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Revenue Share functions
# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# def lifetime_adj_rev_rs(rate, megawatts, year, interest_rate):
#     '''
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts:
#     :param year:
#     :param interest_rate:
#     :return:
#     '''
#     rev_year_y = []
#     for y in range(0, year - 2019):
#         rev_year_y.append(0)
#     for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
#         revenue = (float(rate * megawatts))
#         year_adj_revenue = revenue / ((1 + interest_rate) ** n)
#         rev_year_y.append(year_adj_revenue)
#     return rev_year_y
# def total_adj_rev_rs(years, rate, megawatts, interest_rate):
#     '''
#     :param years:
#     :param rate:
#     :param megawatts:
#     :param effective_rate_list:
#     :param interest_rate:
#     :return:
#     '''
#     total = []  # bin to add present value of lifetime tax revenue from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # calculate yearly list of cash flows for new builds in year yr
#         year_y = years[yr]
#         megawatts_y = megawatts[yr]
#         year_y_lifetime_cash = lifetime_adj_rev_rs(rate, megawatts_y, year_y, interest_rate)
#         # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
#         for n in range(0, len(year_y_lifetime_cash)):
#             y_life = year_y_lifetime_cash[n] / ((1 + interest_rate) ** (year_y - 2020))
#             total[n] = total[n] + y_life
#     total.pop(0)
        
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
#     return total
    
    
# def lifetime_cashflow_rs(rate, megawatts, year, interest_rate):
#     '''
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts: size in MW of all new solar projects >5MW built in locality during particular calendar year
#     :param year: calendar year in which the investment is being made
#     :param interest_rate:  rate at which values will be discounted
#     :return: list of revenues from solar projects >5MW built in indicated year through 2050
#     '''
#     rev_year_y = []
#     for y in range(0, year - 2019):
#         rev_year_y.append(0)
#     for n in range(0, 2051 - year):  # tax revenue from end of 10 years through 2050
#         revenue = (float(rate * megawatts))
#         rev_year_y.append(revenue)
#     return rev_year_y
# def total_cashflow_rs(years, rate, megawatts, interest_rate):
#     '''
#     :param years: list of years in which there is expected to be new investments in solar for a locality
#     :param rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
#     :param megawatts: list of size in MW of total solar investments >5MW in locality for each indicated year 
#     :param interest_rate: rate at which values will be discounted
#     :return:  list of yearly tax revenue from solar projects >5MW built in a locality out to 2050
#     '''
#     total = []  # bin to add present value of lifetime tax revenue from each year to
#     for n in range(0, 32):
#         # create a list of 31 zeros to represent the cashflow of no solar development for the years 2020-2050 (inclusive)
#         total.append(0)
#     for yr in range(0, len(years)):
#         # calculate yearly list of cash flows for new builds in year yr
#         year_y = years[yr]
#         megawatts_y = megawatts[yr]
#         year_y_lifetime_cash = lifetime_cashflow_rs(rate, megawatts_y, year_y, interest_rate)
#         # calculate each year into 2020 $'s and then add to corresponding year on total cashflow
#         for n in range(0, len(year_y_lifetime_cash)):
#             y_life_pv = year_y_lifetime_cash[n] / ((1 + 0) ** (2020 - 2020))
#             total[n] = total[n] + y_life_pv
            
#     total.pop(0) # remove 2019 place holder
    
#     for val in range(0, len(total)): # round final numbers to nearest thousand
#         total[val] = round(total[val] / 1000)
        
#     return total






