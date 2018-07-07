from .test_settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'circleci',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
