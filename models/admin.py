from django.contrib import admin

from .models import Locality, Simulation, Calculations, UserProfile

admin.site.register(Locality)
admin.site.register(Simulation)
admin.site.register(Calculations)
admin.site.register(UserProfile)
# Register your models here.
