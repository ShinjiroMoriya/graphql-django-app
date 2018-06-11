import os
import sys
import platform
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'y3^^67h#j^&daw*(b3(v(=$hqq!j425-paqe3_pc@9!&^(l)&('
DEBUG = os.environ.get('DEBUG', None) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'graphene_django',
    'account',
    'item',
]

if 'local' in platform.node():
    INSTALLED_APPS += [
        'sslserver',
    ]

MIDDLEWARE = [
    'graphqlapp.access_restriction.AccessRestrictionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

HOST_WHITELIST = os.environ.get(
    'HOST_WHITELIST', '').split(',')

GRAPHENE = {
    'SCHEMA': 'graphqlapp.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
    ],
}

ROOT_URLCONF = 'graphqlapp.urls'

WSGI_APPLICATION = 'graphqlapp.wsgi.application'

if TESTING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }

LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': ['templates']
    },
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
)

FERNET_KEY = 'RpPX49a9uUKYSz63CC20wIVfsMEQRwe2Ua1WFz6NlqI='

EMAIL_BACKEND = 'sgbackend.SendGridBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
IP_LIMIT = os.environ.get('IP_LIMIT', None) == 'True'
IPWARE_TRUSTED_PROXY_LIST = os.environ.get(
    'IPWARE_TRUSTED_PROXY_LIST', '').split(',')

LOGGING = {
    'version': 1,
    'formatters': {
        'all': {
            'format': '\t'.join([
                "[%(levelname)s]",
                "asctime:%(asctime)s",
                "module:%(module)s",
                "message:%(message)s",
            ])
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'all'
        },
    },
    'loggers': {
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # },
        'command': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
