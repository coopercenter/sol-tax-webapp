from django.urls import path
from .views import NewSimulationView, UpdateUserParameterView
from django.contrib.auth import views as auth_views
# from models.dash_apps.finished_apps import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', NewSimulationView.as_view(), name='form'),
    path('dash/', views.form_dash, name='dash'),
    path('locality-list/', views.index_page, name='locality-list'),
    path('formtext/', views.request_page, name='test'),
    # path('chart/', views.chart, name="chart"),
    #path('locality-<str:locality_name>/', views.locality_home, name='locality_home'),
    # path('locality-<str:locality_name>/<int:simulation_id>/', views.dash, name='simulation_dash'),
    # path('locality-<str:locality_name>/update-locality-parameters/', UpdateLocalityParameterView.as_view(), name='update_locality'),
    # path('locality-<str:locality_name>/update-depreciation-schedules/', views.depreciationUpdate, name='update_depreciation'),
    path('user-<str:username>/update-user-parameters/', UpdateUserParameterView.as_view(), name='update_user'),
    path('user-<str:username>/update-depreciation-schedules/', views.depreciationUpdate, name='update_depreciation'),
    path('user-<str:username>/', views.user_home, name='locality_home'),
    path('user-<str:username>/<int:simulation_id>/', views.dash, name='simulation_dash'),
    path('profile/', views.profile, name="profile"),
    path('localityName/', views.localityName, name='localityName'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path('password/', views.change_password, name="change_password"),
    path('pdf-<str:locality_name>/', views.testPDF, name="pdf"),
    path('signup/', views.signup, name="signup"),
    path('update-user-<str:username>/', views.update_user, name="update_user"),
    
    path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]