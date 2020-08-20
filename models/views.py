from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from django.views import generic
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

def request_page(request):
    locality_name = request.POST.get('generateButton')
    return render(request, 'testing.html' , {'county': locality_name})

class IndexView(generic.ListView):
    template_name = 'locality-list.html'
    context_object_name = 'all_locality_list'

    def get_queryset(self):
        return Locality.objects.order_by('name')

class NewSimulationView(CreateView):
    # model = Simulation
    # form_class = SimulationForm
    # template_name = 'form.html'


    def post(self, request):
        locality_name = request.POST.get('generateButton')
        form_class = SimulationForm() 
        form_class.fields['locality'].initial = Locality.objects.get(name = locality_name).id
        form_class.fields['locality'].disabled = True
        return render(request, 'form.html', {'form' : form_class, 'county': locality_name})
