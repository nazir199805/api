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

ALLOWED_HOSTS = ["*"]



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
    'JWT_AUTH_SAMESITE':"None",
    'JWT_AUTH_SECURE':True,
}

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'unfold',
    "admin_dashboard.apps.AdminDashboardConfig",
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'users',
    'rest_framework',
    'corsheaders',
    'dj_rest_auth',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',
    'taggit',
    "image_uploader_widget",
    'import_export',
    
    
]

MIDDLEWARE = [
    
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dz5f84b93',
    'API_KEY': '582624146413474',
    'API_SECRET':"_86w2oWZTnRhj0p_zlqakWQvm8E",
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

WSGI_APPLICATION = 'Api.wsgi.application'


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     'https://react-chi-peach.vercel.app',  
#     'https://tashya-mendez.onrender.com',
#     'http://localhost:3000',  
#     'http://localhost:5173',
# ]


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


CSRF_COOKIE_HTTPONLY = False

AUTHENTICATION_BACKENDS = [
   
    'django.contrib.auth.backends.ModelBackend',    
    'allauth.account.auth_backends.AuthenticationBackend',
]

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}






CSRF_TRUSTED_ORIGINS = [
    'https://react-chi-peach.vercel.app',
    "https://localhost",
    "https://tashya-mendez.onrender.com",
    'https://127.0.0.1',
    'http://localhost:5173',

]





GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('FACEBOOK_CLIENT_ID')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.environ.get("PAYPAL_SECRET")
PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com" 



EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'resetdjango8@gmail.com'
# EMAIL_HOST_PASSWORD = 'lkbv usgq snba mziv'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'resetdjango8@gmail.com' 


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
from django.templatetags.static import static

UNFOLD = {
    "DASHBOARD_CALLBACK": "users.views.dashboard_callback",
    "SHOW_LANGUAGES": True,
    "SITE_ICON": {
        "light": lambda request: static("hero/logo.png"),  # light mode
        "dark": lambda request: static("hero/logo.png"),  # dark mode
    },
     "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("hero/logo.png"),
            
        },
     ],
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

    
    "BORDER_RADIUS": "12px",

"COLORS": {
    # Neutral base — soft, balanced grays (for backgrounds, cards, borders, etc.)
    "base": {
        "50":  "oklch(98% 0.002 270)",   # almost white
        "100": "oklch(96% 0.004 270)",
        "200": "oklch(91% 0.006 270)",
        "300": "oklch(86% 0.008 270)",
        "400": "oklch(70% 0.010 270)",
        "500": "oklch(55% 0.012 270)",
        "600": "oklch(43% 0.013 270)",
        "700": "oklch(33% 0.012 270)",
        "800": "oklch(25% 0.010 270)",
        "900": "oklch(17% 0.008 270)",   # near black
        "950": "oklch(10% 0.006 270)",
    },

    # Amber primary — warm golden hues (for buttons, icons, accents)
    "primary": {
        "50":  "oklch(98% 0.03 85)",
        "100": "oklch(95% 0.05 85)",
        "200": "oklch(90% 0.09 85)",
        "300": "oklch(84% 0.13 85)",
        "400": "oklch(75% 0.17 85)",
        "500": "oklch(68% 0.20 85)",  # main amber
        "600": "oklch(61% 0.19 85)",
        "700": "oklch(52% 0.16 85)",
        "800": "oklch(44% 0.13 85)",
        "900": "oklch(36% 0.10 85)",
        "950": "oklch(26% 0.08 85)",
    },

    # Font mapping (links text tone to base scale automatically)
    "font": {
        "subtle-light": "var(--color-base-500)",
        "subtle-dark": "var(--color-base-400)",
        "default-light": "var(--color-base-700)",
        "default-dark": "var(--color-base-200)",
        "important-light": "var(--color-base-900)",
        "important-dark": "var(--color-base-50)",
    },
},



    "SIDEBAR": {
        "show_search": True,
        "command_search": True,  
        "show_all_applications": True,  
         "STYLES": [
            lambda request: static("css/style.css"),
    ],
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
                 
                ],
            },
            
        ],
    
    },
}
    


   

