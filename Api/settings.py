
import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%sgu-!itv9-q^qtel#c1#9n)u(%d1-i@gsbv$ab_bi@(@up!0f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'tashya-mendez.onrender.com',
    'localhost',
    '127.0.0.1'
]



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}



REST_USE_JWT = True

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    'JWT_AUTH_SAMESITE':"none",
    'JWT_AUTH_SECURE':True,
}

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'unfold',
    "admin_dashboard.apps.AdminDashboardConfig",
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'users',
    'rest_framework',
    # 'rest_framework.authtoken',
    'corsheaders',
    'dj_rest_auth',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    # 'social_django',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',
    'taggit',
    "image_uploader_widget",
    'import_export',
    
    
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
    'django.middleware.locale.LocaleMiddleware',
    # 'middleware.CrossOriginMiddleware',
]

ROOT_URLCONF = 'Api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates',
                 BASE_DIR / 'venv/Lib/site-packages/unfold/templates',],
        
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
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',  
#     'https://your-frontend-url.com',  
# ]

CSRF_COOKIE_HTTPONLY = False

AUTHENTICATION_BACKENDS = [
   
    'django.contrib.auth.backends.ModelBackend',    
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}



# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
#             'secret': os.environ.get('GOOGLE_SECRET'),
#             'key': ''
#         }
#     }
# }


CSRF_TRUSTED_ORIGINS = [
    "https://localhost:3000",
    "https://tashya-mendez.onrender.com",
    'https://127.0.0.1',

]

CSRF_COOKIE_HTTPONLY = False  





EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "nazirsherzad12345@gmail.com"  

ACCOUNT_LOGIN_METHODS = ["email"]






# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': 'cxtPtWuFncJeJsduWqunBhckNxDTzwEP',
#         'HOST': 'mainline.proxy.rlwy.net',
#         'PORT': '15098',
#     }
# }

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


# ACCOUNT_SIGNUP_FIELDS = {
#     'username': {
#         'required': False,  # Change this based on your preference
#     },
#     'email': {
#         'required': True,  # This means the email is required during signup
#     }
# }


LANGUAGES = (
    ("de", ("German")),
    ("en", ("English")),
)


from django.urls import reverse_lazy
import static

UNFOLD = {
    "DASHBOARD_CALLBACK": "users.views.dashboard_callback",
    "SHOW_LANGUAGES": True,
    "SITE_TITLE": "About You",
    "SITE_HEADER": "About You Admin",
    "SITE_SUBHEADER": "Welcome to your site admin",
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": "/",
        },
    ],
    

    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,

    
    "BORDER_RADIUS": "6px",

"COLORS": {
    "primary": {
        "50": "#fffbeb",
        "100": "#fef3c7",
        "200": "#fde68a",
        "300": "#fcd34d",
        "400": "#fbbf24",
        "500": "#f59e0b",  # main amber
        "600": "#d97706",
        "700": "#b45309",
        "800": "#92400e",
        "900": "#78350f",
        "950": "#451a03",
    },
    "font": {
        "subtle-light": "var(--color-base-500)",
        "subtle-dark": "var(--color-base-400)",
        "default-light": "var(--color-base-600)",
        "default-dark": "var(--color-base-300)",
        "important-light": "var(--color-base-900)",
        "important-dark": "var(--color-base-100)",
    },
},


    "SIDEBAR": {
        "show_search": True,
        "command_search": True,  
        "show_all_applications": True,  
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {   
                "title": _("User Management"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Profiles"),
                        "icon": "person",
                        "link": reverse_lazy("admin:users_profile_changelist"),
                    },
                    {
                        "title": _("Notifications"),
                        "icon": "notifications",
                        "link": reverse_lazy("admin:users_notification_changelist"),
                    },
                ],
            },
            {
                "title": _("Store"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy("admin:users_product_changelist"),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:users_category_changelist"),
                    },
                    {
                        "title": _("Tags"),
                        "icon": "sell",
                        "link": reverse_lazy("admin:taggit_tag_changelist"),
                    },
                    {
                        "title": _("Favorites"),
                        "icon": "favorite",
                        "link": reverse_lazy("admin:users_favorite_changelist"),
                    },
                ],
            },
            {
                "title": _("Cart"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": _("Carts"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:users_cart_changelist"),
                    },
                    {
                        "title": _("Cart Items"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:users_cartitem_changelist"),
                    },
                ],
            },
            {
                "title": _("Frontend CMS"),
                "collapsible": True,
                "separator": True,
                "items": [
                    {
                        "title": _("Hero Images"),
                        "icon": "image",
                        "link": reverse_lazy("admin:users_heroimage_changelist"),
                    },
                    {
                        "title": _("Hero Buttons"),
                        "icon": "radio_button_checked",
                        "link": reverse_lazy("admin:users_herobutton_changelist"),
                    },
                    {
                        "title": _("API Content"),
                        "icon": "code",
                        "link": reverse_lazy("admin:users_api_changelist"),
                    },
                    {
                        "title": _("Offers"),
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:users_offer_changelist"),
                    },
                ],
            },
        ],
    
}


   
}

