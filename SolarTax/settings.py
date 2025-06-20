"""
Django settings for SolarTax project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

"""
import django_heroku
import os
import dj_database_url
import psycopg2
# from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
if os.path.exists('hiddenVars/secret_key.txt'):
    with open('hiddenVars/secret_key.txt') as f:
        SECRET_KEY = f.read().strip()
else:
    SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: Don't run with debug turned on in production!

if os.path.exists('hiddenVars'):
    DEBUG = True
    ALLOWED_HOSTS = ['https://solar-tax-webapp-dev.azurewebsites.net', '127.0.0.1:8000', 'localhost:8000']
else:
    DEBUG = False
    ALLOWED_HOSTS = ['solar-tax-webapp.azurewebsites.net', 'https://solar-tax-webapp-dev.azurewebsites.net', 'localhost:8000', '127.0.0.1:8000']
# ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'models.apps.ModelsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    'channels_redis',
    'crispy_forms',
    'crispy_bootstrap4', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'SolarTax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins':[
                'models.templatetags.custom_tags',
            ]
        },
    },
]

# WSGI_APPLICATION = 'SolarTax.wsgi.application'
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


if os.path.exists('hiddenVars/azure_name.txt') :
    with open('hiddenVars/azure_name.txt') as f:
        NAME = str(f.read().strip())
else:
    NAME = os.environ['NAME']  

if os.path.exists('hiddenVars/azure_user.txt'):
    with open('hiddenVars/azure_user.txt') as f:
        USER = str(f.read().strip())
else:
    USER = os.environ['USER']   

if os.path.exists('hiddenVars/azure_password.txt'):
    with open('hiddenVars/azure_password.txt') as f:
        PASSWORD = str(f.read().strip())
else:
    PASSWORD = os.environ['PASSWORD']    

if os.path.exists('hiddenVars/azure_host.txt'):
    with open('hiddenVars/azure_host.txt') as f:
        HOST = str(f.read().strip())
else:
    HOST = os.environ['HOST'] 

if os.path.exists('hiddenVars/azure_port.txt'):
    with open('hiddenVars/azure_port.txt') as f:
        PORT = str(f.read().strip())
else:
    PORT = os.environ['PORT'] 

    


DATABASES = {
     'default': { 
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': NAME,
         'USER': USER,
         'PASSWORD': PASSWORD,
         'HOST': HOST,
         'PORT': PORT,
     }
 }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASGI_APPLICATION = 'SolarTax.routing.applications'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG':{
            'hosts': [{'localhost', '8000'}],
        }
    }
}

STATIC_FINDERS ={
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.plotly.dash.finders.DashAssestFinder',
    'django.plotly.dash.finders.DashComponentFinder'
}

PLOTLY_COMPONENTS=[
    'dash_core_components',
    'dash_html_components',
    'dash_renderer',
    'dpd_components'
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'localityName'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'VaSolar@virginia.edu'
EMAIL_HOST_PASSWORD = 'hdwprsfxxnjedphc'
# if os.path.exists('hiddenVars/email.txt'):
#     with open('hiddenVars/email.txt') as f:
#         EMAIL_HOST_USER = str(f.read().strip())
# else:
#     EMAIL_HOST_USER = str(os.environ['EMAIL_HOST_USER'])

# if os.path.exists('hiddenVars/email_password.txt'):
#     with open('hiddenVars/email_password.txt') as f:
#         EMAIL_HOST_PASSWORD = str(f.read().strip())
# else:
#     EMAIL_HOST_PASSWORD= str(os.environ['EMAIL_HOST_PASSWORD'])
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

try:
    # Configure Django App for Heroku.
    import django_heroku
    django_heroku.settings(locals())
except ImportError:
    found = False

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"  
CRISPY_TEMPLATE_PACK = 'bootstrap4' 

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGIN = ['https://solar-tax-webapp.azurewebsites.net', 'https://solar-tax-webapp-dev.azurewebsites.net']