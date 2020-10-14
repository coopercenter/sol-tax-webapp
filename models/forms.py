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
        fields = ('locality', 'initial_year', 'initial_investment', 'project_size', 'total_acreage', 'inside_fence_acreage', 'baseline_land_value', 'inside_fence_land_value', 'dominion_or_apco')
        labels = {
            'initial_investment': ugettext_lazy('Initial Investment ($)'),
            'project_size': ugettext_lazy('Project Size (MW)'),
            'total_acreage': ugettext_lazy('Total Project acreage (Acres)'),
            'inside_fence_acreage': ugettext_lazy('Solar Project Inside the Fence (Acres)'),
            'baseline_land_value': ugettext_lazy('Baseline Value of Land ($)'),
            'inside_fence_land_value': ugettext_lazy('Inside the Fence Value of Land ($)'),
            'dominion_or_apco': ugettext_lazy('Is the project operated by either Dominion or APCO?'),
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
            'dominion_or_apco': forms.CheckboxInput(attrs={'style': 'width:30px;height:35px;position:relative;top: 10px; margin:0 20px;'}),
        }

class LocalityUpdateForm(forms.ModelForm):
    class Meta:
        model = Locality
        fields = ('revenue_share_rate', 'discount_rate', 'mt_tax_rate', 'real_property_rate', 'assessment_ratio', 'baseline_true_value', 'adj_gross_income', 'taxable_retail_sales', 'population', 'adm', 'required_local_matching', 'budget_escalator', 'years_between_assessment')
        labels = {
            'revenue_share_rate': ugettext_lazy("Revenue Share Rate ($/MW)"), 
            'discount_rate': ugettext_lazy("Discount Rate (%)"), 
            'mt_tax_rate': ugettext_lazy("M&T Tax Rate ($/ $100 Assessed Value"), 
            'real_property_rate': ugettext_lazy("Real Property Rate ($/ $100 Assessed Value"), 
            'assessment_ratio': ugettext_lazy("Assessment Ratio (%)"), 
            'baseline_true_value': ugettext_lazy("Baseline True Value ($)"), 
            'adj_gross_income': ugettext_lazy("Adjusted Gross Income ($)"), 
            'taxable_retail_sales': ugettext_lazy("Taxable Retail Sales ($)"), 
            'population': ugettext_lazy("Population"), 
            'adm': ugettext_lazy("Average Daily Student Membership (ADM)"), 
            'required_local_matching': ugettext_lazy("Required Local Matching ($)"), 
            'budget_escalator': ugettext_lazy("Budget Escalator ($)"), 
            'years_between_assessment': ugettext_lazy("Years Between Assessment"),
        }
        widgets = {
            'revenue_share_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':1400}),
            'discount_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'mt_tax_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'real_property_rate': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'assessment_ratio': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'baseline_true_value': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'adj_gross_income': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'taxable_retail_sales': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'population': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'adm': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'required_local_matching': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'budget_escalator': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':100}),
            'years_between_assessment': forms.NumberInput(attrs={'class': 'form-control', 'min':1, 'max':30}),
        }