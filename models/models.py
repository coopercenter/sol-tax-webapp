from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse
from django.db.models import UniqueConstraint

def mt_tax_default():
    print(list(0 for i in range(0, 30)))
    return list(0 for i in range(0, 30))

class Locality(models.Model):
    name = models.CharField(max_length=200)
    discount_rate = models.IntegerField(default = 6)
    revenue_share_rate = models.IntegerField(default = 1400)
    mt_tax_rate = ArrayField(models.FloatField(), size = 31, default=list)
    real_propery_rate = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.name



class Simulation(models.Model):
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE)
    initial_investment = models.IntegerField(default = 100000000)
    initial_year = models.IntegerField(default = 2021)
    # revenue_share_rate = models.IntegerField(default = 1400)
    project_size = models.IntegerField(default = 100)
    # discount_rate = models.IntegerField(default = 6)
    
    def __str__(self):
        return self.locality.name + str(self.initial_investment)
    
    def get_absolute_url(self):
        return reverse('dash')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["locality", "initial_investment", "initial_year", "project_size"], name="unique_locality_simulation")
        ]

    

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
