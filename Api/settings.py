
import os
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%sgu-!itv9-q^qtel#c1#9n)u(%d1-i@gsbv$ab_bi@(@up!0f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}


REST_USE_JWT = True
REST_AUTH = {
    "USE_JWT": True, 
    "TOKEN_MODEL": None,
}

REST_USE_JWT = True


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'rest_framework',
    # 'rest_framework.authtoken',
    'corsheaders',
    'dj_rest_auth',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'social_django',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',
    'taggit',
]

MIDDLEWARE = [
    
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'Api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Api.wsgi.application'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_ALL_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["*"]

AUTHENTICATION_BACKENDS = [
   
    'django.contrib.auth.backends.ModelBackend',    
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}




CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]

CSRF_COOKIE_HTTPONLY = False  



SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # literally this string
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")

DEFAULT_FROM_EMAIL = 'nazirsherzad12345@gmail.com'  


INTERNAL_IPS = [
    "127.0.0.1",  # Localhost
]




ACCOUNT_LOGIN_METHODS = ["email"]






# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'cxtPtWuFncJeJsduWqunBhckNxDTzwEP',
        'HOST': 'mainline.proxy.rlwy.net',
        'PORT': '15098',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# MEDIA_URL  = '/media/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SOCIALACCOUNT_STORE_TOKENS = True


ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*', 'first_name', 'last_name'] 

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None

JAZZMIN_SETTINGS = {
    "site_title": "My Admin",
    "site_header": "My Admin Panel",
    "site_brand": "About You",
    "welcome_sign": "Welcome to My Admin",
    "site_logo": None,  # You can set a logo here if you want
    "copyright": "About You ©",
    
    

    # === Customize icons ===
    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        # Add your models here with desired orange-colored icons
        # Use FontAwesome classes
    },

   
  
}

JAZZMIN_UI_TWEAKS = {
    "sidebar_nav_bg": "#1e1e1e",         # Dark sidebar background
    "sidebar_nav_active_bg": "#ff6600",  # Orange active item background
    "sidebar_nav_active_color": "#fff", # Active text color
    "sidebar_nav_color": "#ccc",         # Sidebar text color
    "sidebar_nav_hover_color": "#ff6600", # Hover text color (orange)
}
