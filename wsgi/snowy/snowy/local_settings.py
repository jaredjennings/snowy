import os

# Local Django settings for snowy project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'snowy',
        'USER': os.getenv('OPENSHIFT_POSTGRESQL_DB_USERNAME'),
        'PASSWORD': os.getenv('OPENSHIFT_POSTGRESQL_DB_PASSWORD'),
        'HOST': os.getenv('OPENSHIFT_POSTGRESQL_DB_HOST'),
        'PORT': os.getenv('OPENSHIFT_POSTGRESQL_DB_PORT'),
    }
}

# Fill in this information from
# http://recaptcha.net/api/getkey?app=snowy
#RECAPTCHA_ENABLED = False
#RECAPTCHA_PUBLIC_KEY = ''
#RECAPTCHA_PRIVATE_KEY = ''

EMAIL_PORT = 1025

# Uncomment for limited user access
#MODERATE_NEW_USERS = True

# Uncomment for HTTPS
URI_SCHEME = 'https'

SECRET_KEY = os.getenv('OPENSHIFT_GEAR_UUID')
