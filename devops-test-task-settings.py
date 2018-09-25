DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "yrunner",
        'USER': "dev",
        'PASSWORD': "dev_password",
        'HOST': "127.0.0.1",
        'PORT': "5432",
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'default': {
            'format': '[%(asctime)s][%(levelname)s] - %(pathname)s - %(message)s',
    }},
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': "yrunner.log",
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 20,
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'default',
            'filename': "yrunner_error.log",
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 20,
        },

    },
    'loggers': {
        'django': {
            'handlers': ["file", "file_error"],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
