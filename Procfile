release: python manage.py migrate
web: gunicorn SolarTax.wsgi
clock: python models/feedback_sender.py