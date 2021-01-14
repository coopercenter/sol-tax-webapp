# Package Scheduler.
from apscheduler.schedulers.background import BackgroundScheduler
from .models import Feedback
from datetime import *
from django.core.mail import send_mail

# Main cronjob function.
# sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds = 30)
# def timed_job():
#     print('This job runs every 30 seconds')

# # Create an instance of scheduler and add function.
# # scheduler = BlockingScheduler()
# # scheduler.add_job(cronjob, "interval", seconds=30)

# sched.start()

def print_update():
    #If monday get any feedback from 3pm friday to 3pm monday
    if(datetime.now().isoweekday() == 1):
    # test = Feedback.objects.filter(date__lte=datetime.now() and date__gt=datetime.now()-timedelta(days=3))
    # print(datetime.now() - timedelta(days=3))
    # test = Feedback.objects.filter(date__gte=datetime.now()).filter(date__lt=(datetime.now() - timedelta(days=3)))
    # test = Feedback.objects.filter(date__gt=(datetime.now() - timedelta(days=3)))
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=3)))
    else:
        test = Feedback.objects.filter(date__lte=(datetime.now())).filter(date__gt=(datetime.now() - timedelta(days=1)))
    print(test)

    if test:
        message = ""
        for item in test:
            message += "From: " + str(item.email) + "\n" + "Date/Time: " + str(item.date) + "\n" + item.message + "\n\n"

        send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu', 'emm2t@virginia.edu', 'carrie.hearne@dmme.virginia.gov'], fail_silently=False,)
        #send_mail('Feedback from ' + str(date.today()), message, 'coopercentersoltax@gmail.com', ['tpc3yw@virginia.edu'], fail_silently=False,)
        print("sent_mail")



def cronjob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=15, minute=22, second=0)
    #scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second + 5)
    scheduler.start()