release: python manage.py collectstatic --noinput && python manage.py migrate
web: gunicorn SolarTax.wsgi
clock: python feedback_sender.py