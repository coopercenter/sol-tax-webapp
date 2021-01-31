release: python manage.py migrate
web: gunicorn SolarTax.asgi
clock: python feedback_sender.py