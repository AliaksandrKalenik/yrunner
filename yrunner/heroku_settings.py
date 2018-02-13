from yrunner.settings import *


import django_heroku
django_heroku.settings(locals())
BROKER_URL = os.environ.get('RABBITMQ_BIGWIG_URL', 'amqp://guest:guest@localhost//')
