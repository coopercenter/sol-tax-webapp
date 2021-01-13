from django.contrib import admin

from .models import Locality, Simulation, Calculations, UserProfile, Feedback

admin.site.register(Locality)
admin.site.register(Simulation)
admin.site.register(Calculations)
admin.site.register(UserProfile)
admin.site.register(Feedback)
###
#  Adds the models of this project to the admin site so anyone on the admin site can see all information about instances of models that have
#  been created. Any new models that are added to models.py, need to be included here to view in the admin site.
###
