# Package Scheduler.
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')

application = get_asgi_application()

import django
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SolarTax.settings')
django.setup()
# import django
# django.setup()

from apscheduler.schedulers.background import BackgroundScheduler
from feedback_worker import print_update

scheduler = BackgroundScheduler()

scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=14, minute=7, second=0)

scheduler.start()


    #scheduler.add_job(print_update, 'cron', day_of_week='mon-fri', hour=datetime.now().hour, minute=datetime.now().minute, second=datetime.now().second + 5)
