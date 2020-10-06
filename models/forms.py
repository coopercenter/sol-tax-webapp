from django import forms
from django.forms import ModelForm
from .models import Simulation, Locality
from django.utils.translation import ugettext_lazy


# class SelectForm(forms.Form):
#     locality = forms.ModelChoiceField(queryset=Locality.objects.all())
#     widget = forms.Select(attrs={'onchange': 'this.form.submit();'})


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ('locality', 'initial_year', 'initial_investment', 'project_size', 'total_acreage', 'inside_fence_acreage', 'baseline_land_value', 'inside_fence_land_value',)
        labels = {
            'initial_investment': ugettext_lazy('Initial Investment ($)'),
            'project_size': ugettext_lazy('Project Size (MW)'),
            'total_acreage': ugettext_lazy('Total Project acreage (Acres)'),
            'inside_fence_acreage': ugettext_lazy('Solar Project Inside the Fence (Acres)'),
            'baseline_land_value': ugettext_lazy('Baseline Value of Land ($)'),
            'inside_fence_land_value': ugettext_lazy('Inside the Fence Value of Land ($)')
        }
        widgets = {
            'locality': forms.HiddenInput(),
            'initial_year': forms.NumberInput(attrs={'class': 'form-control', 'min':2020, 'max':2050}),
            'initial_investment': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'project_size': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'total_acreage': forms.NumberInput(attrs={'class': 'form-control', 'min':100, 'max':10000}),
            'inside_fence_acreage': forms.NumberInput(attrs={'class': 'form-control', 'min':100, 'max':10000}),
            'baseline_land_value': forms.NumberInput(attrs={'class': 'form-control', 'min':100}),
            'inside_fence_land_value': forms.NumberInput(attrs={'class': 'form-control', 'min':100}),
        }