from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.views import generic
from .models import Locality, Simulation
from .forms import SimulationForm 
from django.core import serializers


def index(request):
    return render(request, 'index.html')

# def selectLocality(request):
#     if request.method == 'POST':
#         form = SelectForm(request.POST)
#         if form.is_valid():
#             return render_to_response('/form/', )
# def form(request):
#     if request.method == 'POST':
#         form = SimulationForm(request.POST)
#         if form.is_valid():
#             return render(request, 'dash.html')
#     else:
#         form = SimulationForm()

#     return render(request, 'form.html', {'form': form})

def dash(request):
    if request.method == 'POST':
        form = SimulationForm(request.POST)
        # print(request.POST['locality'])
        # print()
        # print(form.errors)
        # print(form.is_valid())
        if form.is_valid():
            simulation = form.save(commit = False)
            # print(Locality.objects.get(id = request.POST['locality']))
            simulation.locality = Locality.objects.get(id = request.POST['locality'])
            simulation.initial_investment = request.POST['initial_investment']
            simulation.initial_year = request.POST['initial_year']
            simulation.revenue_share_rate = request.POST['revenue_share_rate']
            simulation.project_size = request.POST['project_size']
            simulation.discount_rate = request.POST['discount_rate']
            simulation.save()
            sim = serializers.serialize("python", Simulation.objects.filter(id = simulation.id))
            loc = Locality.objects.filter(name = simulation.locality)[0].name
            print(loc)
            return render(request, 'dash.html', {'simulation':sim, 'locality':loc})
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
