# Package Scheduler.
import os
from django.core.asgi import get_asgi_application
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')
application = get_asgi_application()
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from models.models import Feedback
from datetime import *
from django.core.mail import send_mail
import time
import requests

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour="9-17", minute="0, 30, 59")
def ping_site():
    requests.get("https://solar-tax-webapp.herokuapp.com/")

@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=15, minute=0)
def print_update():
    if(datetime.now().isoweekday() == 1):
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=3)))
    else:
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=1)))

    if test:
        message = ""
        for item in test:
            message += "From: " + str(item.email) + "\n" + "Date/Time: " + str(item.date) + "\n" + item.message + "\n\n"

        if not os.path.exists('hiddenVars'): # FOR use with Heroku
            email_1 = os.environ['STAKEHOLDER_EMAIL_1']
            email_2 = os.environ['STAKEHOLDER_EMAIL_2']
            email_3 = os.environ['STAKEHOLDER_EMAIL_3']

            send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', [email_1, email_2, email_3], fail_silently=False,)
        
        #For use on local server, enter your email in the brackets inside quotes
        #send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['YOUR EMAIL HERE'], fail_silently=False,)

scheduler.start()

