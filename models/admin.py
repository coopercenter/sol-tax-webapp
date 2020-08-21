from django.contrib import admin

from .models import Locality, Simulation, Calculations

admin.site.register(Locality)
admin.site.register(Simulation)
admin.site.register(Calculations)
# Register your models here.
