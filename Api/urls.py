from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.registration.views import RegisterView
from users.serializers import CustomRegisterSerializer
from users.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('api/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('custom/login/', CustomLoginView.as_view(),name='customLogin'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', RegisterView.as_view(serializer_class=CustomRegisterSerializer)),
   

    ]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)