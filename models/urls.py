from django.urls import path
from .views import NewSimulationView
# from models.dash_apps.finished_apps import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', NewSimulationView.as_view(), name='form'),
    path('dash/', views.dash, name='dash'),
    path('locality-list/', views.IndexView.as_view(), name='locality-list'),
    path('formtext/', views.request_page, name='test'),
    path('chart/', views.chart, name="chart")
]