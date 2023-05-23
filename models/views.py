from matplotlib import pylab
from pylab import *

from .models import Locality, Simulation, Calculations, UserProfile, Feedback
from .forms import SimulationForm, UserProfileUpdateForm, SignUpForm, PasswordResetUsernameForm, FeedbackForm
from .revenue_calculations import *

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.views import generic
from django.views.generic import CreateView, ListView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.core import serializers
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from plotly.offline import plot

import plotly.graph_objects as go
import urllib, base64
import PIL, PIL.Image, io
import csv


def create_csv_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    if UserProfile.objects.filter(name= str(request.user)).exists():
        user = UserProfile.objects.get(name= str(request.user))
    else:
        return render(request, '404.html')
    user_dict = user.__dict__
    user_simulation = Simulation.objects.filter(user = user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(request.user) +'"SolTax_Results.csv"'

    writer = csv.writer(response)
    writer.writerow([str(request.user) + " Solar Project Analyses"])
    writer.writerow([''])

    writer.writerow(['Project Revenue'])
    writer.writerow([''])
    writer.writerow(['Project', 'M&T Revenue', 'Revenue Share', 'Increase From Revenue Share'])
    total_mt = 0
    total_rs = 0
    for sim in user_simulation:
        calc = Calculations.objects.get(simulation = sim)
        mt = round(sum(calc.tot_mt)*1000, -3)
        total_mt += mt
        rs = round(sum(calc.tot_rs)*1000, -3)
        total_rs += rs
        writer.writerow([sim.name, mt, rs, rs-mt])

    writer.writerow(['Totals', total_mt, total_rs, total_rs-total_mt])
    writer.writerow([''])
    writer.writerow(['Projects'])
    writer.writerow([''])

    for sim in user_simulation:
        writer.writerow([sim.name])
        sim_dict = sim.__dict__
        writer.writerow([item for item in sim_dict if item not in ("id", "_state", "user_id")])
        writer.writerow(sim_dict[item] for item in sim_dict if item not in ("id", "_state", "user_id"))

        calc = Calculations.objects.get(simulation = sim)

        writer.writerow([''])
        writer.writerow(['Yearly Project Breakdown'])
        writer.writerow([' '] + [i for i in range(sim.initial_year, sim.initial_year+sim.project_length)])
        writer.writerow(['M&T Nominal Revenue'] + [round(value*1000, -3) for value in calc.cas_mt])
        writer.writerow(['Revenue Share Nominal Revenue'] + [round(value*1000, -3) for value in calc.cas_rs])
        writer.writerow(['M&T Discounted Revenue'] + [round(value*1000, -3) for value in calc.tot_mt])
        writer.writerow(['Revenue Share Discounted Revenue'] + [round(value*1000, -3) for value in calc.tot_rs])
        writer.writerow([''])
    
    writer.writerow([''])
    writer.writerow(['User Parameters'])
    
    for field in user_dict:
        if field != "id" and field != "_state" and ("depreciation" not in field):
            writer.writerow([field, user_dict[field]])

    writer.writerow([''])
    writer.writerow(['Depreciation Schedules'])
    writer.writerow(["Year"] + [i+1 for i in range(len(user_dict["local_depreciation"]))])
    writer.writerow(["Local Depreciation"] + [user_dict["local_depreciation"][i] for i in range(len(user_dict["local_depreciation"]))])
    writer.writerow(["SCC Depreciation"] + [user_dict["scc_depreciation"][i] for i in range(len(user_dict["scc_depreciation"]))])

    writer.writerow([''])
    writer.writerow(['Revenue Share Rates'])
    writer.writerow(["Year"] + [2021, 2026, 2031, 2036, 2041, 2046, 2051, 2056, 2061])
    writer.writerow(["Revenue Share Rate"] + [user_dict["revenue_share_rate"][i] for i in range(len(user_dict["revenue_share_rate"]))])

    return response

# Landing Page
def index(request):
    return render(request, 'index.html')

# 404 Error Page
def custom_404_error(request, exception):
    return render(request, '404.html')

# Login Page
def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # Form submitted
            user = form.get_user()
            login(request, user) # Check Login Information
            return HttpResponseRedirect('/user-' + str(user)+'/') # Redirect to locality's home page
        else:
            messages.error(request, 'Username or Password is incorrect')
            return HttpResponseRedirect('/login/')
    else: # Displays Login Form
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout, redirects to landing page
def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

#SignUp
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            new_user_profile = UserProfile(name = username)
            new_user_profile.save()

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect("/update-user-"+username+"/")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def update_user(request, username):
    # if request.method == 'POST':
        
    localities = Locality.objects.order_by('name')
    return render(request, 'select_locality.html', {'all_localities': localities, 'username':username})

def commentPage(request):
    if request.method == 'GET':
        form = FeedbackForm()
    else:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            organization = form.cleaned_data['organization']
            message = form.cleaned_data['message']

            feedback_instance = Feedback.objects.create(email = email, message = message, name = name, organization = organization, date= timezone.now())
            feedback_instance.save()
            return redirect("feedback-success")
    return render(request, "feedback.html", {'form': form})

def commentSuccessPage(request):
    return render(request, "feedback_success.html")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def localityName(request):
    if(request.POST.get('locality')):
        locality = (request.POST.get('locality'))
    return HttpResponseRedirect('/locality-'+locality+'/')


def user_home(request, username):
    if request.POST.get('simulation_id'):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        simulation.delete()

    user = UserProfile.objects.get(name = username)
    simulations = user.simulation_set.all()

    remainder = len(simulations) % 6
    if remainder == 3 or remainder == 4:
        gap = "True"
    else:
        gap = "False"
    if request.POST.get('locality'):
        locality_name = request.POST['locality']
        if locality_name != 'Choose Your Locality':
            locality = Locality.objects.get(name=locality_name)
            user.discount_rate = locality.discount_rate
            #user.revenue_share_rate = locality.revenue_share_rate
            user.real_property_rate = locality.real_property_rate
            user.mt_tax_rate = locality.mt_tax_rate
            user.assessment_ratio = locality.assessment_ratio
            user.baseline_true_value = locality.baseline_true_value
            user.adj_gross_income = locality.adj_gross_income
            user.taxable_retail_sales = locality.taxable_retail_sales
            user.population = locality.population
            user.adm = locality.adm
            user.required_local_matching = locality.required_local_matching
            user.budget_escalator = locality.budget_escalator
            user.years_between_assessment = locality.years_between_assessment
            user.use_composite_index = locality.use_composite_index
            user.local_depreciation = locality.local_depreciation
            user.scc_depreciation = locality.scc_depreciation
            depreciation_ext(user.local_depreciation)
            depreciation_ext(user.scc_depreciation)
            user.save()

    if user.mt_tax_rate == 0:
        return HttpResponseRedirect("/update-user-"+user.name+"/")

    if request.POST.get('discount_rate'):
        user.discount_rate = int(request.POST.get('discount_rate'))
        #user.revenue_share_rate = int(request.POST.get('revenue_share_rate'))
        user.mt_tax_rate = float(request.POST.get('mt_tax_rate'))
        user.real_property_rate = float(request.POST.get('real_property_rate'))
        user.assessment_ratio = float(request.POST.get('assessment_ratio'))
        user.baseline_true_value = int(request.POST.get('baseline_true_value'))
        user.adj_gross_income = int(request.POST.get('adj_gross_income'))
        user.taxable_retail_sales = int(request.POST.get('taxable_retail_sales'))
        user.population = int(request.POST.get('population'))
        user.adm = float(request.POST.get('adm'))
        user.required_local_matching = int(request.POST.get('required_local_matching'))
        user.budget_escalator = float(request.POST.get('budget_escalator'))
        user.years_between_assessment = int(request.POST.get('years_between_assessment'))

        if request.POST.get('use_composite_index') == None:
            user.use_composite_index = False
        elif request.POST.get('use_composite_index') == "on":
            user.use_composite_index = True
        user.save()

    if request.POST.get('local-1'):
        local = []
        for item in request.POST:
            if item[:5] == "local":
                local.append(float(request.POST.get(item))/100)
        user.local_depreciation = local[:35]
        user.save()

    if request.POST.get('scc-1'):
        scc = []
        for item in request.POST:
            if item[:3] == "scc":
                scc.append(float(request.POST.get(item))/100)
        user.scc_depreciation = scc
        user.save()

    if request.POST.get('rs-2021'):
        new_rs = []
        max_rs = [1400, 1540, 1694, 1863, 2050, 2255, 2480, 2728, 3001]
        for item in request.POST:
            print(item)
            print(request.POST.get(item))
            if item != 'csrfmiddlewaretoken':
                new_rs.append(float(request.POST.get(item)))
        for i in range(len(new_rs)):
            if(new_rs[i] > max_rs[i]):
                years = [2021, 2026, 2031, 2036, 2041, 2046, 2051, 2056, 2061]
                data = zip(years, user.revenue_share_rate)
                return render(request, 'revenue_share_update.html', {'current_values': data, 'locality': user.name, 'error': 'For the year ' +  str((2021 + i*5)) + ' you entered ' + str(new_rs[i]) + ', however the maximum value allowed is ' + str(max_rs[i]) + '. Please try again.'})
        user.revenue_share_rate = new_rs
        user.save()

    total_mt = 0
    total_rs = 0
    for simulation in simulations:
        calc = performCalculations(user, simulation)
        calc.save()
        simulation.calculations = calc
        total_mt += sum(calc.tot_mt)*1000
        total_rs += sum(calc.tot_rs)*1000
        simulation.save()
    total_mt = round(total_mt, -3)
    total_rs = round(total_rs, -3)
    difference = total_rs - total_mt
    
    user.save()

    rs_years = [2021, 2026, 2031, 2036, 2041, 2046, 2051, 2056, 2061]
    rs_data = zip(user.revenue_share_rate, rs_years)
    return render(request, 'locality-home.html', {'locality': user, 'simulations':simulations, 'total_rs_revenue':total_rs, 'total_mt_revenue':total_mt, 'difference':difference, 'gap':gap, 'rs_data':rs_data})


# Creates Scatter Plot using plotly
def scatter(mt, rs, simulation):
    starting_year = simulation.initial_year
    project_length = simulation.project_length
    x1 = [i + starting_year for i in range(project_length)]
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

def form_dash(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit = False)
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = UserProfile.objects.filter(name = simulation.user)[0]
            return HttpResponseRedirect("/user-" + loc.name + '/' + str(simulation.id) + '/')
        else:
            if form.has_error('NON_FIELD_ERRORS'):
                return HttpResponse("Error this analysis has already been created, go back to the Locality page to view the analysis with these parameters")
            else:
                form_class = SimulationForm()
                username = UserProfile.objects.get(id = request.POST.get('user')).name
                form_class.fields['user'].initial = request.POST.get('user')
                form_class.fields['name'].initial = request.POST.get('name')
                form_class.fields['initial_year'].initial = request.POST.get('initial_year')
                form_class.fields['project_length'].initial = request.POST.get('project_length')
                form_class.fields['initial_investment'].initial = request.POST.get('initial_investment')
                form_class.fields['project_size'].initial = request.POST.get('project_size')
                form_class.fields['total_acreage'].initial = request.POST.get('total_acreage')
                form_class.fields['inside_fence_acreage'].initial = request.POST.get('inside_fence_acreage')
                form_class.fields['baseline_land_value'].initial = request.POST.get('baseline_land_value')
                form_class.fields['inside_fence_land_value'].initial = request.POST.get('inside_fence_land_value')
                form_class.fields['outside_fence_land_value'].initial = request.POST.get('outside_fence_land_value')
                form_class.fields['dominion_or_apco'].initial = request.POST.get('dominion_or_apco')                
                messages.error(request, 'Total project acreage was less than inside the fence acreage.')
                return render(request, 'create_new_analysis_form.html', {'form' : form_class, 'county': username})
    else:
        return HttpResponse('Error please select fill out the model generation form')

def dash(request, username, simulation_id):
    user = UserProfile.objects.get(name = username)
    if user.mt_tax_rate == 0:
        return HttpResponseRedirect("/update-user-"+user.name+"/")

    if(request.method == 'GET'):
        simulation = Simulation.objects.get(pk = simulation_id)
        sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
        loc = UserProfile.objects.get(name = username)

        calc = performCalculations(loc, simulation)
        calc.save()

        context = {
            'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation),
            'plot2': scatter(calc.cas_mt, calc.cas_rs, simulation)
        }

        return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    if(request.POST.get('simulation_id')):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
        loc = UserProfile.objects.filter(name = simulation.user)[0]

        calc = performCalculations(loc, simulation)
        calc.save()

        context = {
            'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation),
            'plot2': scatter(calc.cas_mt, calc.cas_rs, simulation)
        }

        return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit = False)
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = UserProfile.objects.filter(name = simulation.user)[0]
        
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation),
                'plot2': scatter(calc.cas_mt, calc.cas_rs, simulation)
            }
            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
        
        else:
            simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = UserProfile.objects.filter(name = simulation.user)[0]
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation),
                'plot2': scatter(calc.cas_mt, calc.cas_rs, simulation)
            }

            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    else:
        return HttpResponse('Error please select fill out the model generation form')
# Create your views here.

def request_page(request):
    locality_name = request.POST.get('generateButton')
    return render(request, 'testing.html' , {'county': locality_name})

class NewSimulationView(CreateView):

    # def get(self, request):
        
    def post(self, request):
        if(request.POST.get('viewButton') == None):
            username = request.POST.get('generateButton')
            form_class = SimulationForm() 
            form_class.fields['user'].initial = UserProfile.objects.get(name = username).id
            return render(request, 'create_new_analysis_form.html', {'form' : form_class, 'county': username})
        else:
            return HttpResponseRedirect('/' + request.POST.get('viewButton'))

class UpdateUserParameterView(CreateView):
    
    def post(self, request, username):
        if(request.POST.get('viewButton') == None):
            form_class = UserProfileUpdateForm()
            user = UserProfile.objects.get(name = username) 
            #form_class.fields['revenue_share_rate'].initial = user.revenue_share_rate
            form_class.fields['discount_rate'].initial = user.discount_rate
            form_class.fields['mt_tax_rate'].initial = user.mt_tax_rate
            form_class.fields['real_property_rate'].initial = user.real_property_rate
            form_class.fields['assessment_ratio'].initial = user.assessment_ratio
            form_class.fields['baseline_true_value'].initial = user.baseline_true_value
            form_class.fields['adj_gross_income'].initial = user.adj_gross_income
            form_class.fields['taxable_retail_sales'].initial = user.taxable_retail_sales
            form_class.fields['population'].initial = user.population
            form_class.fields['adm'].initial = user.adm
            form_class.fields['required_local_matching'].initial = user.required_local_matching
            form_class.fields['budget_escalator'].initial = user.budget_escalator
            form_class.fields['years_between_assessment'].initial = user.years_between_assessment
            form_class.fields['use_composite_index'].initial = user.use_composite_index
            return render(request, 'update_form.html', {'form' : form_class, 'county': username})
        else:
            return HttpResponse("ERROR")

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordResetUsernameView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetUsernameForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)

def depreciationUpdate(request, username):
    user = UserProfile.objects.get(name = username)
    scc = user.scc_depreciation
    depreciation_ext(scc)
    scc=scc[:35]
    local = user.local_depreciation
    depreciation_ext(local)

    return render(request, 'depreciation_schedules.html', {'local_depreciation': local, 'scc_depreciation': scc, 'locality': username})

def revenueShareUpdate(request, username):
    user = UserProfile.objects.get(name = username)
    rs = user.revenue_share_rate
    years = [2021, 2026, 2031, 2036, 2041, 2046, 2051, 2056, 2061]
    data = zip(years, rs)

    return render(request, 'revenue_share_update.html', {'current_values': data, 'locality': username})

def performCalculations(locality, simulation):

    '''
    Simulation Variables
    '''
    local_investment = simulation.initial_investment
    initial_year = simulation.initial_year
    project_length = simulation.project_length
    project_size = simulation.project_size
    total_project_acreage = simulation.total_acreage
    inside_fence_acreage =simulation.inside_fence_acreage
    outside_fence_acreage = total_project_acreage - inside_fence_acreage
    baseline_land_value = simulation.baseline_land_value
    inside_fence_land_value = simulation.inside_fence_land_value
    outside_fence_land_value = simulation.outside_fence_land_value
    dominion_or_apco = simulation.dominion_or_apco

    '''
    Locality Variables
    '''
    use_composite_index = locality.use_composite_index
    discount_rate = int(locality.discount_rate)/100
    #revenue_share_rate = int(locality.revenue_share_rate)
    # revenue_share_rate = 1400

    revenue_share_rate = locality.revenue_share_rate
    adjusted_rs_rate = []
    if initial_year >= 2021:
        for i in range(initial_year, initial_year + project_length):
            index = (i - 2021) // 5
            adjusted_rs_rate.append(revenue_share_rate[index])
    else:
        adjusted_rs_rate = [revenue_share_rate[0] for i in range(project_length)]
    print(adjusted_rs_rate)
    #     if(i % 5 == 1 and i != 1):
    #         revenue_share_rate.append(revenue_share_rate[i-1] * 1.1)
    #     else:
    #         revenue_share_rate.append(revenue_share_rate[i-1])
    # revenue_share_rate = [round(elem, 0) for elem in revenue_share_rate]


    mt_tax_rate = locality.mt_tax_rate
    real_property_rate = locality.real_property_rate
    assessment_ratio = locality.assessment_ratio/100
    local_baseline_true_value = locality.baseline_true_value
    local_adj_gross_income = locality.adj_gross_income
    local_taxable_retail_sales = locality.taxable_retail_sales
    local_population = locality.population
    local_adm = locality.adm
    required_local_matching = locality.required_local_matching
    budget_escalator = locality.budget_escalator/100
    years_between_assessment = locality.years_between_assessment
    local_depreciation = locality.local_depreciation
    scc_depreciation = locality.scc_depreciation
    effective_rate_ext(scc_depreciation, project_length)
    effective_rate_ext(local_depreciation, project_length)

    '''
    State Variables
    '''
    state_true_value = [1170092111098.94 for i in range(project_length)]
    state_adj_gross_income = 269067675604.708
    state_taxable_retail_sales = 100207273998.18
    state_adm = 1239781.3
    state_population = 8382993
    mt_stepdown = [.8, .8, .8, .8, .8, .7, .7, .7, .7, .7, .6]
    effective_rate_ext(mt_stepdown, project_length)


    if(project_size < 25 and not dominion_or_apco):
        effective_tax_rate = [mt_tax_rate for i in range(project_length)]
        effective_exemption_rate = mt_stepdown
        effective_depreciation_schedule = local_depreciation
    elif((project_size >= 25 or dominion_or_apco) and project_size < 150):
        effective_tax_rate = [real_property_rate for i in range(project_length)]
        effective_exemption_rate = mt_stepdown
        effective_depreciation_schedule = scc_depreciation
    else:
        effective_tax_rate = [real_property_rate for i in range(project_length)]
        effective_exemption_rate = [0 for i in range(project_length)]
        effective_depreciation_schedule = scc_depreciation
    '''
    Land Value Calculations
    '''

    current_value_of_land = current_land_value(total_project_acreage, baseline_land_value, initial_year, project_length, years_between_assessment)
    current_revenue_from_land = current_land_revenue(current_value_of_land, real_property_rate)  

    solar_project_valuation = solar_facility_valuation(initial_year, local_investment, effective_exemption_rate, effective_depreciation_schedule, assessment_ratio, project_length)

    new_value_land = new_land_value(total_project_acreage, inside_fence_acreage, outside_fence_acreage, inside_fence_land_value, outside_fence_land_value, initial_year, project_length, years_between_assessment)
    land_value_increase = increase_in_land_value(current_value_of_land, new_value_land, assessment_ratio)
    increase_in_gross_revenue = increased_county_gross_revenue_from_project(solar_project_valuation, effective_tax_rate, land_value_increase, real_property_rate)

    mt_and_property_income = total_gross_revenue_mt(current_revenue_from_land, increase_in_gross_revenue)

    taxable_property_increase = increase_in_taxable_property(land_value_increase, solar_project_valuation)

    '''
    M&T Tax Calculations
    '''  

    adm_gross_income = get_gross_income_adm(local_adj_gross_income, local_adm, state_adj_gross_income, state_adm, project_length)
    adm_retail_sales = get_retail_sales_adm(local_taxable_retail_sales, local_adm, state_taxable_retail_sales, state_adm, project_length)
    per_capita_gross_income = get_gross_income_per_capita(local_adj_gross_income, local_population, state_adj_gross_income, state_population, project_length)
    per_capita_retail_sales = get_retail_sales_per_capita(local_taxable_retail_sales, local_population, state_taxable_retail_sales, state_population, project_length)

    base_adm_true_values = get_baseline_true_values_adm(local_baseline_true_value, local_adm, state_true_value, state_adm)
    base_per_capita_true_values = get_baseline_true_values_per_capita(local_baseline_true_value, local_population, state_true_value, state_population)

    base_adm_composite = adm_composite_index(base_adm_true_values, adm_gross_income, adm_retail_sales)
    base_local_composite = per_capita_composite_index(base_per_capita_true_values, per_capita_gross_income, per_capita_retail_sales)
    
    base_composite_index = composite_index(base_adm_composite, base_local_composite)

    local_project_true_values = local_true_values(local_baseline_true_value, taxable_property_increase)
    state_project_true_values = state_total_true_values(state_true_value, taxable_property_increase)

    project_adm_true_values = get_true_values_adm(local_project_true_values, local_adm, state_project_true_values, state_adm)
    project_per_capita_true_values = get_true_values_per_capita(local_project_true_values, local_population, state_project_true_values, state_population)

    project_adm_composite = adm_composite_index(project_adm_true_values, adm_gross_income, adm_retail_sales)
    project_local_composite = per_capita_composite_index(project_per_capita_true_values, per_capita_gross_income, per_capita_retail_sales)

    project_composite_index = composite_index(project_adm_composite, project_local_composite)

    locality_education_budget = required_local_matching / base_composite_index[0]

    base_required_education_contribution = baseline_required_education_contribution(locality_education_budget, budget_escalator, base_composite_index)
    project_required_education_contribution = pv_required_education_contribution(locality_education_budget, budget_escalator, project_composite_index)

    local_contribution_increase = increase_in_local_contribution(project_required_education_contribution, base_required_education_contribution)
    print("composite indeces " + str(project_adm_composite) + str(project_local_composite))
    print(str(land_value_increase))

    net_revenue  = net_total_revenue_from_project(mt_and_property_income, local_contribution_increase)

    adj_net_revenue = []
    for i in range(project_length):
        if i % years_between_assessment == 0:
            if(not use_composite_index):
                adj_net_revenue.append(mt_and_property_income[i]/1000)
            else:
                adj_net_revenue.append(net_revenue[i]/1000)
        else:
            adj_net_revenue.append(adj_net_revenue[i -1])

    cas_mt = adj_net_revenue
    tot_mt = total_adj_rev(cas_mt, discount_rate, initial_year)


    '''
    Revenue Share Calculations
    '''

    project_value_with_real_property = [local_baseline_true_value + land_value_increase[i] for i in range(len(land_value_increase))]

    real_property_true_values_adm = get_true_values_adm(project_value_with_real_property, local_adm, state_true_value, state_adm)
    project_real_property_adm_composite = adm_composite_index(real_property_true_values_adm, adm_gross_income, adm_retail_sales)

    real_property_true_values_per_capita = get_true_values_per_capita(project_value_with_real_property, local_population, state_true_value, state_population)
    project_real_property_local_composite = per_capita_composite_index(real_property_true_values_per_capita, per_capita_gross_income, per_capita_retail_sales)

    project_real_property_composite_index = composite_index(project_real_property_adm_composite, project_real_property_local_composite)
    project_real_property_education_contribution = pv_required_education_contribution(locality_education_budget, budget_escalator, project_real_property_composite_index)
    
    real_property_increase_in_local_contribution = [project_real_property_education_contribution[i] - base_required_education_contribution[i] for i in range(len(project_real_property_education_contribution))]
    real_property_tax_revenue = [real_property_rate * land_value_increase[i]/100 for i in range(len(land_value_increase))]

    real_property_increase_in_revenue = net_total_revenue_from_project(real_property_tax_revenue, real_property_increase_in_local_contribution)
    revenue_share_income = total_cashflow_rs(adjusted_rs_rate, project_size, initial_year, project_length)
    revenue_share_total = [current_revenue_from_land[i] + revenue_share_income[i] + real_property_increase_in_revenue[i] for i in range(len(revenue_share_income))]

    cas_rs = []
    for i in range(project_length):
        if i % years_between_assessment == 0:
            if(not use_composite_index):
                cas_rs.append((current_revenue_from_land[i] + revenue_share_income[i] + real_property_tax_revenue[i])/1000)
            else:
                cas_rs.append(revenue_share_total[i]/1000)
        else:
            cas_rs.append(cas_rs[i - 1])

    tot_rs = total_adj_rev(cas_rs, discount_rate, initial_year)

    try:
        sim = simulation.calculations
        calc = Calculations.objects.get(simulation=simulation)
        calc.cas_mt = cas_mt
        calc.cas_rs = cas_rs
        calc.tot_mt = tot_mt
        calc.tot_rs = tot_rs
        calc.save()
    except Calculations.DoesNotExist:
        calc = Calculations.objects.create(simulation=simulation, cas_mt = cas_mt, cas_rs=cas_rs, tot_mt=tot_mt, tot_rs=tot_rs)
    return calc