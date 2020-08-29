import os
# import ast
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seconds_in_a_week = 7 * 24 * 60 * 60

# SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = "vmr*6c^2kud@((fe_b8pmkl^h3)_7)wr1bu3b$xj5hym7whj8o"
DEBUG = True  # ast.literal_eval(os.environ.get('DJANGO_DEBUG', 'True'))

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = ['*']

FILE_UPLOAD_PERMISSIONS = 0o644

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = ('localhost:3000', '167.172.101.50',)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'easy_thumbnails',
    'rest_framework',
    # 'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf',
    'django_extensions',
    'project',
    'project.base.apps.tags'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# DATABASES = {
#     'default': {
#          'ENGINE': 'django.db.backends.postgresql_psycopg2',
#          'NAME': os.environ.get("POSTGRES_DB"),
#          'USER': os.environ.get("POSTGRES_USER"),
#          'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
#          'HOST': os.environ.get("POSTGRES_HOST"),
#          'PORT': os.environ.get("POSTGRES_PORT"),
#      }
#  }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "postgres",
        'USER': "postgres",
        'PASSWORD': "postgres",
        'HOST': "database",
        'PORT': 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',
#                            'project.apps.utils.auth_backends.EmailBackend']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/'

STATIC_URL = '/static-files/'
MEDIA_URL = '/media-files/'
STATIC_ROOT = '/static-files'
MEDIA_ROOT = '/media-files'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=300),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# ELASTICSEARCH_DSL = {
#     'default': {
#         'hosts': 'elasticsearch:9200'
#     },
# }
