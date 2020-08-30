from django.urls import path
from .views import NewSimulationView
# from models.dash_apps.finished_apps import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', NewSimulationView.as_view(), name='form'),
    path('dash/', views.dash, name='dash'),
    path('locality-list/', views.index_page, name='locality-list'),
    path('formtext/', views.request_page, name='test'),
    path('chart/', views.chart, name="chart"),
    path('table/', views.table, name="table"),
    path('locality-<str:locality_name>/', views.locality_home, name='locality_home')
]