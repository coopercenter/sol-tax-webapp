from matplotlib import pylab
from pylab import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.views.generic import CreateView, ListView
from django.views import generic
from .models import Locality, Simulation, Calculations, UserProfile
from .forms import SimulationForm, UserProfileUpdateForm, SignUpForm, PasswordResetUsernameForm
from django.core import serializers
import urllib, base64
import PIL, PIL.Image, io
from django.db.models import Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator

from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_protect

from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Frame, BaseDocTemplate, Paragraph
from reportlab.platypus.tables import Table
from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from plotly.offline import plot
import plotly.graph_objects as go

from django.core.mail import send_mail
from django.conf import settings

# Landing Page
def index(request):
    #return redirect_no_parameters(request)
    return render(request, 'index.html')

# Login Page
def loginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # Form submitted
            user = form.get_user()
            login(request, user) # Check Login Information
            return HttpResponseRedirect('/user-' + str(user)+'/') #redirect to locality's home page
    #else: # Displays Login Form
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout, redirects to landing page
def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

def update_user_profile(request, user_profile):
    return HttpResponse("TESTING")

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
    if request.method == 'POST':
        print("testing")
        
    localities = Locality.objects.order_by('name')
    return render(request, 'select_locality.html', {'all_localities': localities, 'username':username})

def testPDF(request, locality_name):
    locality = Locality.objects.get(name = locality_name)
    height = defaultPageSize[1]
    width = defaultPageSize[0]
    buffer = io.BytesIO()

    # p = canvas.Canvas(buffer)
    # p.setFont("Times-Roman", 20)
    # #p.drawCenteredString(width/2, height, locality_name)
    # p.drawCenteredString(width/2-100, height-80, "SolTax Analysis for " + locality_name)
    # print(locality.simulation_set.all())
    # for simulation in locality.simulation_set.all():
    #     table = Table(["Years", str(simulation.initial_year) + " - " + str(simulation.initial_year + simulation.project_length)])
    #     p.append(table)
    # p.showPage()
    # p.save()
    #response = HttpResponse(mimetype='application/pdf')
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    elements = []

    doc = SimpleDocTemplate(response, rightMargin=0, leftMargin=6.5 * 2.54, topMargin=0.3 * 2.54, bottomMargin=0)
    frame_left = Frame(width/2, height, width/2, height, showBoundary = 1) 
    #elements.append(frame_left)
    tables = []
    canvas = Canvas("test.pdf")
    
    style = getSampleStyleSheet()
    style = ParagraphStyle(
        'small',
        parent = style['Normal'],
        fontSize = 20,
        alignment = TA_CENTER,
        spaceBefore = 50,
        trailing = 50,
        leading = 50,
    )
    #print(style['Normal'])
    #style['fontSize'] = 20

    title = Paragraph('''<strong> SolTax Analysis for ''' + locality_name + ''' </strong>''', style)
    
    #print(ParagraphStyle)
    elements.append(title)
    
    locality_info_data = [
        [Paragraph('''<strong> Parameter </strong>'''), Paragraph('''<strong> Value </strong>''')],
        ["Using Composite Index for Calculations?", locality.use_composite_index],
        ["Revenue Share Rate", "$" + str('{:,}'.format(locality.revenue_share_rate)) + "/MW"],
        ["Discount Rate", str(locality.discount_rate) + "%"],
        ["M&T Tax Rate", "$" + str(locality.mt_tax_rate) + "/$100 Assessed Value"],
        ["Real Property Rate", "$" + str(locality.real_property_rate) + "/$100 Assessed Value"],
        ["Assessment Ratio", str(locality.assessment_ratio) + "%"],
        [Paragraph(''' <strong> Composite Index Parameters </strong> ''')],
        ["Local True Value", "$" + str('{:,}'.format(locality.baseline_true_value))],
        ["Adjusted Gross Income", "$" + str('{:,}'.format(locality.adj_gross_income))],
        ["Taxable Retail Sales", "$" + str('{:,}'.format(locality.taxable_retail_sales))],
        ["Population", str('{:,}'.format(locality.population))],
        ["ADM", str('{:,}'.format(locality.adm))],
        ["Required Local Matching", "$" + str('{:,}'.format(locality.required_local_matching))],
        ["Education Budget Escalator", str(locality.budget_escalator) + "%"],
        ["Years Between Assessment", str(locality.years_between_assessment)],
    ] 
    locality_info_table = Table(locality_info_data, colWidths = 200, rowHeights = 20)
    elements.append(locality_info_table)

    for simulation in locality.simulation_set.all():
        mt_tot = round(sum(simulation.calculations.tot_mt)*1000, -3)
        rs_tot = round(sum(simulation.calculations.tot_rs)*1000, -3)
        data = [
            [Paragraph('''<strong> Parameter </strong>'''), Paragraph('''<strong> Value </strong>''')],
            #["Parameter", "Value"],
            ["Years", str(simulation.initial_year) + " - " + str(simulation.initial_year + simulation.project_length)],
            ["Initial Investment", "$" + '{:,}'.format(simulation.initial_investment)],
            ["Project Size", str(simulation.project_size) + "MW"],
            ["Dominion or APCO", simulation.dominion_or_apco],
            ["Revenue Share Revenue", "$" + '{:,}'.format(rs_tot)],
            ["M&T Revenue", "$" + '{:,}'.format(mt_tot)],
            ["Difference", "$" + '{:,}'.format(rs_tot - mt_tot)],
        ]
        table = Table(data, colWidths = 150, rowHeights = 30)
        #table.setStyle(TableStyle([('')]))
        elements.append(table)
        tables.append(table)
    frame_left.addFromList(tables, canvas)
    # canvas.showPage()
    # canvas.save()
        #elements.append(table)
    # data=[(1,2),(3,4)]
    # table = Table(data, colWidths=270, rowHeights=79)
    # elements.append(table)
    
    doc.build(elements) 
    canvas.showPage()
    return response

    #buffer.seek(0)
    #return FileResponse(buffer, as_attachment=True, filename="hello.pdf")

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
    print(request.GET)
    if(request.POST.get('locality')):
        locality = (request.POST.get('locality'))
    return HttpResponseRedirect('/locality-'+locality+'/')

# def user_home(request, username):
#     user = UserProfile.objects.get(name=username)
    
#     if request.POST.get('locality'):
#         locality_name = request.POST['locality']
#         if locality_name != 'Choose Your Locality':
#             locality = Locality.objects.get(name=locality_name)
#             user.discount_rate = locality.discount_rate
#             user.revenue_share_rate = locality.revenue_share_rate
#             user.real_property_rate = locality.real_property_rate
#             user.mt_tax_rate = locality.mt_tax_rate
#             user.assessment_ratio = locality.assessment_ratio
#             user.baseline_true_value = locality.baseline_true_value
#             user.adj_gross_income = locality.adj_gross_income
#             user.taxable_retail_sales = locality.taxable_retail_sales
#             user.population = locality.population
#             user.adm = locality.adm
#             user.required_local_matching = locality.required_local_matching
#             user.budget_escalator = locality.budget_escalator
#             user.years_between_assessment = locality.years_between_assessment
#             user.use_composite_index = locality.use_composite_index
#             user.local_depreciation = locality.local_depreciation
#             user.scc_depreciation = locality.scc_depreciation
#             user.save()
#     return HttpResponse("TESITNF")


def user_home(request, username):
    if request.POST.get('simulation_id'):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        simulation.delete()

    #locality = Locality.objects.get(name = locality_name.title())
    #locality = serializers.serialize("python", Locality.objects.filter(name = locality_name.title()))
    user = UserProfile.objects.get(name = username)
    #simulations = locality.simulation_set.all()
    simulations = user.simulation_set.all()

    if request.POST.get('locality'):
        locality_name = request.POST['locality']
        if locality_name != 'Choose Your Locality':
            locality = Locality.objects.get(name=locality_name)
            user.discount_rate = locality.discount_rate
            user.revenue_share_rate = locality.revenue_share_rate
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
            user.save()

    if user.mt_tax_rate == 0:
        return HttpResponseRedirect("/update-user-"+user.name+"/")

    if request.POST.get('discount_rate'):
        print(request.POST.get)
        # locality.discount_rate = int(request.POST.get('discount_rate'))
        # locality.revenue_share_rate = int(request.POST.get('revenue_share_rate'))
        # locality.mt_tax_rate = float(request.POST.get('mt_tax_rate'))
        # locality.real_property_rate = float(request.POST.get('real_property_rate'))
        # locality.assessment_ratio = float(request.POST.get('assessment_ratio'))
        # locality.baseline_true_value = int(request.POST.get('baseline_true_value'))
        # locality.adj_gross_income = int(request.POST.get('adj_gross_income'))
        # locality.taxable_retail_sales = int(request.POST.get('taxable_retail_sales'))
        # locality.population = int(request.POST.get('population'))
        # locality.adm = float(request.POST.get('adm'))
        # locality.required_local_matching = int(request.POST.get('required_local_matching'))
        # locality.budget_escalator = float(request.POST.get('budget_escalator'))
        # locality.years_between_assessment = int(request.POST.get('years_between_assessment'))
        #locality.use_composite_index = request.POST.get('use_composite_index')
        user.discount_rate = int(request.POST.get('discount_rate'))
        user.revenue_share_rate = int(request.POST.get('revenue_share_rate'))
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
        print(local)
        user.local_depreciation = local
        user.save()

    if request.POST.get('scc-1'):
        scc = []
        for item in request.POST:
            if item[:3] == "scc":
                scc.append(float(request.POST.get(item))/100)
        user.scc_depreciation = scc
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
        print(sum(simulation.calculations.tot_rs) - sum(simulation.calculations.tot_mt))
    total_mt = round(total_mt, -3)
    total_rs = round(total_rs, -3)
    difference = total_rs - total_mt
    user.save()
    #simulation.save()
    return render(request, 'locality-home.html', {'locality': user, 'simulations':simulations, 'total_rs_revenue':total_rs, 'total_mt_revenue':total_mt, 'difference':difference})


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
        print(form)
        # print(form)
        print(form.has_error('NON_FIELD_ERRORS'))
        if form.is_valid():
            print("valid")
            simulation = form.save(commit = False)
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            #loc = Locality.objects.filter(name = simulation.locality)[0]
            loc = UserProfile.objects.filter(name = simulation.user)[0]
            print(simulation.id)
            return HttpResponseRedirect("/user-" + loc.name + '/' + str(simulation.id) + '/')
        else:
            return HttpResponse("Error this analysis has already been created, go back to the Locality page to view the analysis with these parameters")
            
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
            'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation)
        }

        return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    if(request.POST.get('simulation_id')):
        simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
        sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
        loc = UserProfile.objects.filter(name = simulation.user)[0]

        calc = performCalculations(loc, simulation)
        calc.save()

        context = {
            'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation)
        }

        return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        if form.is_valid():
            print("form")
            print("valus")
            simulation = form.save(commit = False)
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = UserProfile.objects.filter(name = simulation.user)[0]
        
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation)
            }
            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
        
        else:
            simulation = Simulation.objects.get(id = request.POST.get('simulation_id'))
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = UserProfile.objects.filter(name = simulation.user)[0]
            calc = performCalculations(loc, simulation)
            calc.save()

            context = {
                'plot1': scatter(calc.cas_mt, calc.cas_rs, simulation)
            }

            return render(request, 'dash.html', {'simulation':sim, 'locality':loc, 'calculations':calc, 'n':range(simulation.project_length), "graph":context})
    else:
        return HttpResponse('Error please select fill out the model generation form')
# Create your views here.

def request_page(request):
    locality_name = request.POST.get('generateButton')
    return render(request, 'testing.html' , {'county': locality_name})

# def update_locality_parameters(request, locality_name):
#     if request.method == 'POST':
#         form = LocalityUpdateForm(request.POST)
#         # print(form)
#         print(form.has_error('NON_FIELD_ERRORS'))
#         if form.is_valid():
#             print("valid")
#             locality = form.save(commit = False)
#             locality.save()
#             # sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
#             # loc = Locality.objects.filter(name = simulation.locality)[0]
#             # print(simulation.id)
#             return HttpResponseRedirect("/locality-" + locality.name + "/")
#         else:
#             return HttpResponse("Error in updating locality parameters, please try again")
        
#     else:
#         return HttpResponse('Error please select fill out the model generation form')

class NewSimulationView(CreateView):

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
            # loc_name = username
            form_class = UserProfileUpdateForm()
            user = UserProfile.objects.get(name = username) 
            # form_class.fields['locality'].initial = Locality.objects.get(name = locality_name).id
            # print(locality)
            # form_class.fields['locality'].initial = locality.id
            form_class.fields['revenue_share_rate'].initial = user.revenue_share_rate
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
            #return HttpResponseRedirect('/' + request.POST.get('viewButton'))

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
    scc=scc[:36]
    print("scc")
    print(scc)
    local = user.local_depreciation
    depreciation_ext(local)
    return render(request, 'depreciation_schedules.html', {'local_depreciation': local, 'scc_depreciation': scc, 'locality': username})

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
    revenue_share_rate = int(locality.revenue_share_rate)
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
    #scc_depreciation = [.9, .9, .9, .9, .8973, .8729, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10]
    scc_depreciation = locality.scc_depreciation
    #print(scc_depreciation)
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

    print(effective_depreciation_schedule)
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

    net_revenue  = net_total_revenue_from_project(mt_and_property_income, local_contribution_increase)
    
    # adj_net_revenue = [net_revenue[i]/1000 for i in range(len(net_revenue))]
    #offset = initial_year - 2020
    #adj_net_revenue = [0 for i in range(project_length)]
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
    print(real_property_increase_in_revenue)
    revenue_share_income = total_cashflow_rs(revenue_share_rate, project_size, initial_year, project_length)
    revenue_share_total = [current_revenue_from_land[i] + revenue_share_income[i] + real_property_increase_in_revenue[i] for i in range(len(revenue_share_income))]
    
    # cas_rs = [revenue_share_total[i]/1000 for i in range(31)]
    #offset = initial_year - 2020
    #cas_rs = [0 for i in range(offset)]
    cas_rs = []
    for i in range(project_length):
        if i % years_between_assessment == 0:
            if(not use_composite_index):
                cas_rs.append((current_revenue_from_land[i] + revenue_share_income[i] + real_property_tax_revenue[i])/1000)
            else:
                cas_rs.append(revenue_share_total[i]/1000)
            # else:
            #     cas_rs.append(0)
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

def depreciation_ext(depreciation_schedule):
    '''
    Takes in schedule of effective rates for county + year of initial build
    Extends list with final effective rate to be available for calculations out to 2050
    '''
    last_rate = depreciation_schedule[-1]
    while len(depreciation_schedule) <= 35:
        depreciation_schedule.append(last_rate)

def effective_rate_ext (effective_rate_list, project_length):
    '''
    Takes in schedule of effective rates for county + year of initial build
    Extends list with final effective rate to be available for calculations out to 2050
    '''
    last_rate = effective_rate_list[-1]
    while len(effective_rate_list) <= project_length:
        effective_rate_list.append(last_rate)

'''
FUNCTIONS TO GET TOTAL MT REVENUE GENERATED BY SOLAR FACILITY

'''


##############################################################
# Functions to determine tax rates for project
##############################################################

'''
    Get the exemption rate for the project. If above 150 MW a solar project does not have any exemptions applied. Otherwise it is the M&T stepdown exemption rate
'''
def get_mt_exemption(size_mw, mt_exemption):
    if(size_mw > 150):
        return 0
    else:
        return mt_exemption

'''
    Get the M&T tax rate for the project. If above 20 MW use the real estate rate for the project, otherwise use the mt_tax_rate
'''
def get_mt_tax_rate(size_mw, mt_tax_rate, real_estate_rate):
    if size_mw > 25:
        return real_estate_rate
    else:
        return mt_tax_rate

##############################################################
# Calculations for Valuation of Proposed Solar Facility
##############################################################

def solar_facility_valuation(year, investment, mt_exemption, depreciation_schedule, assessment_ratio, project_length):
    valuation = []
    for i in range(0, project_length):
        # if(i + 2020 >= year):
        after_exemption = investment * (1 - mt_exemption[i])
        after_depreciation = after_exemption * depreciation_schedule[i]
        assessed_facility_valuation = after_depreciation * assessment_ratio
        valuation.append(round(assessed_facility_valuation)) # If the index is at or past the initial year of project
        # else:
        #     valuation.append(0) #If the index is before the initial year of project
    return valuation


##############################################################
# Calculations for increase in Land Value
##############################################################

def current_land_value(total_acreage, baseline_value, starting_year, project_length, years_between_assessment):
    baseline = []
    # offset = starting_year - 2020
    # for i in range(0, offset):
    #     baseline.append(0)
    for i in range(0, project_length):
        if(i % years_between_assessment == 0):
            baseline.append(round(baseline_value * total_acreage * ((1.012)**(i+1))))
        else:
            baseline.append(baseline[i - 1])
    return baseline

def new_land_value(total_acreage, inside_acreage, outside_acreage, inside_fence_value, outside_fence_value, starting_year, project_length, years_between_assessment):
    total = []
    # offset = starting_year - 2020

    # for i in range(0, offset):
    #     total.append(0)

    for i in range(0, project_length):
        if( i % years_between_assessment == 0):
            inside = inside_fence_value * inside_acreage * ((1.012)**(i+1))
            outside = outside_fence_value * outside_acreage * ((1.012)**(i+1))
            total.append(round(inside + outside))
        else:
            total.append(total[i-1])
        
    return total

def increase_in_land_value(current_land_value, new_land_value, assessment_ratio):
    difference = []
    for i in range(0, len(current_land_value)):
        difference.append(round((new_land_value[i] - current_land_value[i]) * assessment_ratio))
    return difference

##############################################################



##############################################################
# Gross Revenue from Project Calculations
##############################################################

def increased_county_gross_revenue_from_project(solar_valuation_list, applied_mt_tax_rate, increase_in_land_value, applied_real_estate_rate):
    gross_revenue_increase = []
    for i in range(0, len(solar_valuation_list)):
        increase_from_solar = (solar_valuation_list[i] * applied_mt_tax_rate[i])/100
        increase_from_land = (increase_in_land_value[i] * applied_real_estate_rate)/100
        gross_revenue_increase.append(round(increase_from_solar + increase_from_land))
    return gross_revenue_increase

def current_land_revenue(current_land_value, applied_real_estate_rate):
    current_revenue = []
    for i in range(len(current_land_value)):
        current_revenue.append(round(current_land_value[i] * (applied_real_estate_rate/100)))
    return current_revenue

def total_gross_revenue_mt(current_revenue, gross_revenue_increase):
    total_revenue = []
    for i in range(len(current_revenue)):
        total_revenue.append(current_revenue[i] + gross_revenue_increase[i])
    return total_revenue
##############################################################

'''
FUNCTIONS TO GET TOTAL TAX AVAILABLE TO LOCALITIES FROM MT TAX
'''

def net_total_revenue_from_project(gross_revenue_project, increase_in_local_contribution):
    net_total_revenue = []
    for i in range(len(gross_revenue_project)):
        net_total_revenue.append(round(gross_revenue_project[i] - increase_in_local_contribution[i],))
    return net_total_revenue

def increase_in_local_contribution(pv_required_education_contribution, baseline_required_education_contribution):
    increase_contribution = []
    for i in range(len(pv_required_education_contribution)):
        increase_contribution.append(pv_required_education_contribution[i] - baseline_required_education_contribution[i])
    return increase_contribution

def pv_required_education_contribution(locality_education_budget, budget_escalator, pv_composite_index):
    pv_education_contribution = []
    for i in range(len(pv_composite_index)):
        pv_education_contribution.append(locality_education_budget * ((1+budget_escalator) ** i) * pv_composite_index[i])
    return pv_education_contribution

def baseline_required_education_contribution(locality_education_budget, budget_escalator, baseline_composite_index):
    baseline_education_contribution = []
    for i in range(len(baseline_composite_index)):
        baseline_education_contribution.append(locality_education_budget * ((1+budget_escalator) ** i) * baseline_composite_index[i])
    return baseline_education_contribution

'''
COMPOSITE INDEX FUNCTIONS
'''

def composite_index(adm_composite_index, per_capita_composite_index):
    final_pv_composite_index = []
    for i in range(len(adm_composite_index)):
        local_composite_index = ((2/3) * adm_composite_index[i]) + ((1/3) * per_capita_composite_index[i])
        value = 0.45 * local_composite_index
        factor = 10.0 ** 4
        final_pv_composite_index.append(math.trunc((value * factor)) / factor)
    return final_pv_composite_index

def adm_composite_index(true_values_adm, gross_income_adm, retail_sales_adm):
    final_adm_composite_index = []
    for i in range(len(true_values_adm)):
        adm_value = .5 * true_values_adm[i] + .4 * gross_income_adm[i] + .1 * retail_sales_adm[i]
        final_adm_composite_index.append(adm_value)
    return final_adm_composite_index

def per_capita_composite_index(true_values_per_capita, gross_income_per_capita, retail_sales_per_capita):
    final_per_capita_composite_index = []
    for i in range(len(true_values_per_capita)):
        per_capita_value = .5 * true_values_per_capita[i] + .4 * gross_income_per_capita[i] + .1 * retail_sales_per_capita[i]
        final_per_capita_composite_index.append(per_capita_value)
    return final_per_capita_composite_index

'''
TRUE VALUE CALCULATIONS
'''
def get_true_values_adm(local_true_values, divisional_adm, statewide_total_true_values, total_state_adm):
    final_true_values = []
    for i in range(len(local_true_values)):
        numerator = local_true_values[i]/divisional_adm
        denominator = statewide_total_true_values[i]/total_state_adm
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_true_values_per_capita(local_true_values, local_pop, statewide_total_true_values, state_pop):
    final_true_values = []
    for i in range(len(local_true_values)):
        numerator = local_true_values[i]/local_pop
        denominator = statewide_total_true_values[i]/state_pop
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_baseline_true_values_adm(baseline_true_values, divisional_adm, baseline_state_true_values, total_state_adm):
    final_true_values = []
    for i in range(len(baseline_state_true_values)):
        numerator = baseline_true_values/divisional_adm
        denominator = baseline_state_true_values[i]/total_state_adm
        final_true_values.append(numerator/denominator)
    return final_true_values

def get_baseline_true_values_per_capita(baseline_true_values, local_pop, baseline_state_true_values, state_pop):
    final_true_values = []
    for i in range(len(baseline_state_true_values)):
        numerator = baseline_true_values/local_pop
        denominator = baseline_state_true_values[i]/state_pop
        final_true_values.append(numerator/denominator)
    return final_true_values

def local_true_values(baseline_true_value, increase_in_taxable_property):
    final_local_true_values = []
    for i in range(len(increase_in_taxable_property)):
        final_local_true_values.append(baseline_true_value + increase_in_taxable_property[i])
    return final_local_true_values

def state_total_true_values(baseline_state_true_value, increase_in_taxable_property):
    final_state_true_values = []
    for i in range(len(increase_in_taxable_property)):
        final_state_true_values.append(baseline_state_true_value[i] + increase_in_taxable_property[i])
    return final_state_true_values

def increase_in_taxable_property(increase_in_land_value, solar_facility_valuation):
    inc_taxable_property = [increase_in_land_value[i] + solar_facility_valuation[i] for i in range(len(solar_facility_valuation))]
    return inc_taxable_property

'''
GROSS INCOME CALCULATIONS
'''
def get_gross_income_adm(adj_gross_income, divisional_adm, statewide_gross_income, total_state_adm, project_length):
    final_gross_income = []
    for i in range(project_length):
        numerator = adj_gross_income/divisional_adm
        denominator = statewide_gross_income/total_state_adm
        final_gross_income.append(numerator/denominator)
    return final_gross_income

def get_gross_income_per_capita(adj_gross_income, local_pop, statewide_gross_income, state_pop, project_length):
    final_gross_income = []
    for i in range(project_length):
        numerator = adj_gross_income/local_pop
        denominator = statewide_gross_income/state_pop
        final_gross_income.append(numerator/denominator)
    return final_gross_income

'''
RETAIL SALES CALCULATIONS
'''
def get_retail_sales_adm(local_taxable_retail_sales, divisional_adm, state_taxable_retail_sales, total_state_adm, project_length):
    final_retail_sales = []
    for i in range(project_length):
        numerator = local_taxable_retail_sales/divisional_adm
        denominator = state_taxable_retail_sales/total_state_adm
        final_retail_sales.append(numerator/denominator)
    return final_retail_sales

def get_retail_sales_per_capita(local_taxable_retail_sales, local_pop, state_taxable_retail_sales, state_pop, project_length):
    final_retail_sales = []
    for i in range(project_length):
        numerator = local_taxable_retail_sales/local_pop
        denominator = state_taxable_retail_sales/state_pop
        final_retail_sales.append(numerator/denominator)
    return final_retail_sales

def total_cashflow_rs(revenue_share_rate, megawatts, year, project_length):
    '''
        :revenue_share_rate: the rate a locality sets for its revenue share (max $1400/MW, though not capped by function)
        :megawatts: Size of solar project
        :year: Starting year of the solar project
        :return: A list of reveneue share revenue generated during each year from 2020-2050, nominal $
    '''
    cashflow_rev = []
    for i in range(0, project_length):
        #if(i + 2020 >= year):
        cashflow_rev.append((revenue_share_rate * megawatts)) # If the index is at or past the initial year of project
        # else:
        #     cashflow_rev.append(0) #If the index is before the initial year of project
    return cashflow_rev


def total_adj_rev(cas, discount_rate, initial_year):
    '''
        :cas_rs: List of revenue generate during each year from 2020-2050, nominal $
        :discount_rate: rate at which revenue values will be discounted
        :return: A list of revenue generated during each year from 2020-2050, 2020 $
    '''
    tot_rs = []
    for i in range(len(cas)):
        tot_rs.append(cas[i] / ((1 + discount_rate)**(i + (initial_year-2020)))) # Present value formula
    return tot_rs
        

