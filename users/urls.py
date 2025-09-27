from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include


router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'offers', views.OfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


