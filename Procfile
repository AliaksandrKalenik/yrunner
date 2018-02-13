release: python manage.py migrate
web: gunicorn yrunner.wsgi --log-file -
worker: celery worker -A yrunner --loglevel=INFO
