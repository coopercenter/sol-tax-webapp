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

# if(datetime.now().hour > 9 and datetime.now().hour < 5):
#     @scheduler.scheduled_jbo('interval', minutes = 30)
#    def 
@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour="9-17", minute="0, 30, 59")
def ping_site():
    requests.get("https://solar-tax-webapp.herokuapp.com/")


@scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute=49)
def print_update():
    if(datetime.now().isoweekday() == 1):
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=3)))
    else:
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=1)))
    print(test)

    if test:
        message = ""
        for item in test:
            message += "From: " + str(item.email) + "\n" + "Date/Time: " + str(item.date) + "\n" + item.message + "\n\n"

        #send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu', 'emm2t@virginia.edu', 'carrie.hearne@dmme.virginia.gov'], fail_silently=False,)
        send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu'], fail_silently=False,)
        print("sent_mail")


# scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=14, minute=7, second=0)

scheduler.start()

