from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Locality(models.Model):
    name = models.CharField(max_length=200)
    # mt_tax_rate = ArrayField(ArrayField(models.IntegerField()))

    class Meta:
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.name

class Simulation(models.Model):
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE)
    initial_investment = models.IntegerField(default = 100000000)
    initial_year = models.IntegerField(default = 2021)
    revenue_share_rate = models.IntegerField(default = 1400)
    project_size = models.IntegerField(default = 100)
    discount_rate = models.IntegerField(default = 6)
    
    def __str__(self):
        return self.locality.name + str(self.initial_investment)
    
    def get_absolute_url(self):
        return reverse('dash')

class Calculations(models.Model):
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE)
    cas_mt = ArrayField(models.IntegerField(null = True, blank= True),  blank=True)
    cas_rs = ArrayField(models.IntegerField(null = True, blank= True),  blank=True)
    tot_mt = ArrayField(models.IntegerField(null = True, blank= True),  blank=True)
    tot_rs = ArrayField(models.IntegerField(null = True, blank= True),  blank=True)

    def __str__(self):
        return self.simulation.__str__() + "Calculations"
    
    class Meta:
        verbose_name_plural = "Calculations"
