import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')

application = get_asgi_application()

import django
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')
# settings.configure(default_settings=models_defaults, DEBUG=True)
django.setup()

from models.models import Feedback
from datetime import *
from django.core.mail import send_mail
import time

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