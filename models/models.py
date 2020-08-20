from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Locality(models.Model):
    name = models.CharField(max_length=200)
    # mt_tax_rate = ArrayField(ArrayField(models.IntegerField()))

    def __str__(self):
        return self.name

class Simulation(models.Model):
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE)
    initial_investment = models.IntegerField()
    initial_year = models.IntegerField()
    revenue_share_rate = models.IntegerField(default = 1400)
    project_size = models.IntegerField()
    discount_rate = models.IntegerField(default = 6)
    
    def __str__(self):
        return self.locality.name + str(self.initial_investment)
    
    def get_absolute_url(self):
        return reverse('dash')