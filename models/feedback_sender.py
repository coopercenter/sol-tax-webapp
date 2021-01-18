# Package Scheduler.
import django
django.setup()

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')
# import django
# django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from models.feedback_worker import print_update

scheduler = BackgroundScheduler()

# Main cronjob function.

# @scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=11, minute=1 , second=0)
# def print_update():
    #If monday get any feedback from 3pm friday to 3pm monday
    # if(datetime.now().isoweekday() == 1):
    #     test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=3)))
    # else:
    #     test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=1)))
    # print(test)

    # if test:
    #     message = ""
    #     for item in test:
    #         message += "From: " + str(item.email) + "\n" + "Date/Time: " + str(item.date) + "\n" + item.message + "\n\n"

    #     #send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu', 'emm2t@virginia.edu', 'carrie.hearne@dmme.virginia.gov'], fail_silently=False,)
    #     send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu'], fail_silently=False,)
    #     print("sent_mail")
# scheduler.add_job(print_update)
scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=11, minute=13, second=0)

scheduler.start()


    #scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second + 5)
