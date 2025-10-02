from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import RegisterView
from users.serializers import CustomRegisterSerializer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('api/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
     path('auth/registration/', RegisterView.as_view(serializer_class=CustomRegisterSerializer)),
    # path('auth/social/', include('dj_rest_auth.social_urls')), 

    ]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)