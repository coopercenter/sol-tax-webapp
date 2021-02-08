from django.urls import path
from .views import NewSimulationView, UpdateUserParameterView
from django.contrib.auth import views as auth_views
# from models.dash_apps.finished_apps import *
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', NewSimulationView.as_view(), name='form'),
    path('dash/', views.form_dash, name='dash'),
    path('formtext/', views.request_page, name='test'),
    path('user-<str:username>/update-user-parameters/', UpdateUserParameterView.as_view(), name='update_user'),
    path('user-<str:username>/update-depreciation-schedules/', views.depreciationUpdate, name='update_depreciation'),
    path('user-<str:username>/', views.user_home, name='locality_home'),
    path('user-<str:username>/<int:simulation_id>/', views.dash, name='simulation_dash'),
    path('localityName/', views.localityName, name='localityName'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path('password/', views.change_password, name="change_password"),
    path('signup/', views.signup, name="signup"),
    path('update-user-<str:username>/', views.update_user, name="update_user"),
    path('reset-password/', views.PasswordResetUsernameView.as_view(), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('feedback/', views.commentPage, name="feedback"),
    path('feedback-success', views.commentSuccessPage, name="feedback-success"),
    # path('test', views.custom_404_error2, name="404"),
]

handler404 = 'models.views.custom_404_error'