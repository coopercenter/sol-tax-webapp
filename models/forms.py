from django import forms
from django.forms import ModelForm
from .models import Simulation, Locality

# class SelectForm(forms.Form):
#     locality = forms.ModelChoiceField(queryset=Locality.objects.all())
#     widget = forms.Select(attrs={'onchange': 'this.form.submit();'})


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ('locality', 'initial_year', 'initial_investment', 'revenue_share_rate', 'project_size', 'discount_rate')
        widgets = {
            'locality': forms.Select(attrs={'class':'form-control', 'editable':'False'}),
            'initial_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_investment': forms.NumberInput(attrs={'class': 'form-control'}),
            'revenue_share_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'project_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control'}),
        }