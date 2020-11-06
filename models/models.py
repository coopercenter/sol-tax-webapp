from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db.models import UniqueConstraint

def mt_tax_default():
    print(list(0 for i in range(0, 30)))
    return list(0 for i in range(0, 30))

def get_scc_depreciation():
    return list([.9, .9, .9, .9, .8973, .8729, .85, .82, .79, .76, .73, .69, .66, .62, .58, .53, .49, .44, .38, .33, .27, .21, .14, .10, .10, .10, .10, .10, .10, .10, .10])

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
    local_depreciation = ArrayField(models.FloatField(blank=True), null=True, blank=True)
    scc_depreciation = ArrayField(models.FloatField(), default=list(get_scc_depreciation()))
    

    class Meta:
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.name



class Simulation(models.Model):
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE)
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
        return self.locality.name + str(self.initial_investment)
    
    def get_absolute_url(self):
        return reverse('dash')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["locality", "initial_investment", "initial_year", "project_length", "project_size", "total_acreage", "inside_fence_acreage", "baseline_land_value", "inside_fence_land_value", "outside_fence_land_value", "dominion_or_apco"], name="unique_locality_simulation")
        ]

    

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
