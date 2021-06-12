from .base import *

DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed
    'rest_framework',
    # 'corsheaders',
    # 'rest_framework.authtoken',

    # created
    'posts',
    'users'
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# cors
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
]

# REST FRAMEWORK
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.SessionAuthentication'
]

DEFAULT_PERMISSION_CLASSES = [
    'rest_framework.permissions.IsAuthenticated',
]

# use when working with separate react app or api testing (swagger, postman)
# if(DEBUG):
#     DEFAULT_AUTHENTICATION_CLASSES += [
#         'social_club.settings.devPermissions.DevAuthentication'
#     ]
#     DEFAULT_PERMISSION_CLASSES += [
#         'rest_framework.permissions.AllowAny',
#     ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_PERMISSION_CLASSES' : DEFAULT_PERMISSION_CLASSES,
}
