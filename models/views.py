from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from .models import Locality, Simulation
from .forms import SimulationForm 


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
    return render(request, 'dash.html')
# Create your views here.


class NewSimulationView(CreateView):
    model = Simulation
    form_class = SimulationForm
    template_name = 'form.html'
    # fields = '__all__'
