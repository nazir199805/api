from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import RegisterView
from users.serializers import CustomRegisterSerializer
from users.views import CustomLoginView
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from users.views import GoogleLogin


urlpatterns = [
    
    path('', include('index.urls')),
    path('api/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('custom/login/', CustomLoginView.as_view(),name='customLogin'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/register/', include('dj_rest_auth.registration.urls')),  # Sign up
    # path('auth/google/', include('allauth.socialaccount.providers.google.urls')),
    path('auth/registration/', RegisterView.as_view(serializer_class=CustomRegisterSerializer)),
    path("i18n/", include("django.conf.urls.i18n")),
   
    ]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)