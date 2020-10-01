from django.urls import path
from .views import NewSimulationView
# from models.dash_apps.finished_apps import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', NewSimulationView.as_view(), name='form'),
    path('dash/', views.form_dash, name='dash'),
    path('locality-list/', views.index_page, name='locality-list'),
    path('formtext/', views.request_page, name='test'),
    # path('chart/', views.chart, name="chart"),
    path('locality-<str:locality_name>/', views.locality_home, name='locality_home'),
    path('locality-<str:locality_name>/<int:simulation_id>/', views.dash, name='simulation_dash'),
    path('profile/', views.profile, name="profile"),
    path('localityName/', views.localityName, name='localityName'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
]