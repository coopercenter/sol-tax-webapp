from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError



def get_scc_depreciation():
    return list([.9, .9, .9, .9, .9, .8729, .8470, .8196, .7906, .7598, .7271, .6925, .6568, .6170, .5758, .5321, .4858, .4367, .3847, .3295, .2711, .2091, .1434, .10, .10, .10, .10, .10, .10, .10, .10, .10, .10, .10, .10, .10, .10])
    
class Feedback(models.Model):
    email = models.EmailField()
    message = models.CharField(max_length=5000)
    name = models.CharField(max_length=200, default="")
    organization = models.CharField(max_length=200, default="")
    date = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name_plural = "Feedback"
    
    def __str__(self):
        return self.email + "- " + str(self.date)

# Model that represents a user, someone who is generating analyses for solar projects
# they are developing.
class UserProfile(models.Model):
    name = models.CharField(max_length=200)
    discount_rate = models.IntegerField(default = 6)
    revenue_share_rate = models.IntegerField(default = 1400)
    real_property_rate = models.FloatField(default=0)
    mt_tax_rate = models.FloatField(default = 0)
    assessment_ratio = models.FloatField(default=100)
    baseline_true_value = models.BigIntegerField(default = 0)
    adj_gross_income = models.BigIntegerField(default = 0)
    taxable_retail_sales = models.BigIntegerField(default = 0)
    population = models.IntegerField(default = 0)
    adm = models.FloatField(default=0)
    required_local_matching = models.IntegerField(default = 0)
    budget_escalator = models.FloatField(default = 0)
    years_between_assessment = models.IntegerField(default = 5)
    use_composite_index = models.BooleanField(default=True)
    local_depreciation = ArrayField(models.FloatField(blank=True), null=True, blank=True)
    scc_depreciation = ArrayField(models.FloatField(), default=list(get_scc_depreciation()))

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.name

# Locality models should not be changed by a user, only by admin. These contain baseline
# information so a user can model their parameters off of an already existing locality parameters
class Locality(models.Model):
    name = models.CharField(max_length=200)
    discount_rate = models.IntegerField(default = 6)
    revenue_share_rate = models.IntegerField(default = 1400)
    real_property_rate = models.FloatField(default=0)
    mt_tax_rate = models.FloatField(default = 0)
    assessment_ratio = models.FloatField(default=100)
    baseline_true_value = models.BigIntegerField(default = 0)
    adj_gross_income = models.BigIntegerField(default = 0)
    taxable_retail_sales = models.BigIntegerField(default = 0)
    population = models.IntegerField(default = 0)
    adm = models.FloatField(default=0)
    required_local_matching = models.IntegerField(default = 0)
    budget_escalator = models.FloatField(default = 0)
    years_between_assessment = models.IntegerField(default = 5)
    use_composite_index = models.BooleanField(default=True)
    local_depreciation = ArrayField(models.FloatField(blank=True), null=True, blank=True, size=35)
    scc_depreciation = ArrayField(models.FloatField(), default=list(get_scc_depreciation()))
    
    class Meta:
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.name

# Simulation model is a specific project analysis with the parameters defined below
class Simulation(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=150, blank=True)
    initial_investment = models.IntegerField(default = 100000000)
    initial_year = models.IntegerField(default = 2021)
    project_length = models.IntegerField(default = 30)
    project_size = models.IntegerField(default = 100)
    total_acreage = models.IntegerField(default = 2000)
    inside_fence_acreage = models.IntegerField(default = 1000)
    baseline_land_value = models.IntegerField(default = 1000)
    inside_fence_land_value = models.IntegerField(default = 10000)
    outside_fence_land_value = models.IntegerField(default = 1000)
    dominion_or_apco = models.BooleanField(default = True)

    def __str__(self):
        return self.user.name + str(self.initial_investment)
    
    def clean(self):
        cleaned_data=super(Simulation, self).clean()
        tot = self.total_acreage
        inside = self.inside_fence_acreage

        if inside > tot:
            raise ValidationError("Inside fence acreage is higher than total project acreage.")
        return cleaned_data
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "initial_investment", "initial_year", "project_length", "project_size", "total_acreage", "inside_fence_acreage", "baseline_land_value", "inside_fence_land_value", "outside_fence_land_value", "dominion_or_apco"], name="unique_locality_simulation")
        ]

# Calculation model is the class that holds the revenue generated for a specific
# simulation. Contains both M&T and Revenue Share revenues.
class Calculations(models.Model):
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE)
    cas_mt = ArrayField(models.FloatField(null = True, blank= True),  blank=True)
    cas_rs = ArrayField(models.FloatField(null = True, blank= True),  blank=True)
    tot_mt = ArrayField(models.FloatField(null = True, blank= True),  blank=True)
    tot_rs = ArrayField(models.FloatField(null = True, blank= True),  blank=True)

    def __str__(self):
        return self.simulation.__str__() + "Calculations"
    
    class Meta:
        verbose_name_plural = "Calculations"
