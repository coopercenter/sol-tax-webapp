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
        fields = ('locality', 'initial_year', 'initial_investment', 'revenue_share_rate', 'project_size', 'discount_rate')
        labels = {
            'revenue_share_rate': ugettext_lazy('Revenue Share Rate ($/MW)'),
            'project_size': ugettext_lazy('Project Size (MW)'),
            'discount_rate': ugettext_lazy('Discount Rate (%)')
        }
        widgets = {
            'locality': forms.HiddenInput(),
            'initial_year': forms.NumberInput(attrs={'class': 'form-control', 'min':2020, 'max':2050}),
            'initial_investment': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'revenue_share_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':1400}),
            'project_size': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
        }