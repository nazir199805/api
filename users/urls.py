from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', views.ApiViewSet)
router.register(r'offers', views.OfferViewSet)
router.register(r'hero', views.HeroImageViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'favorites', views.FavoriteViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'notifications', views.NotificationViewSet)
router.register(r'sections', views.SectionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('products/filter', views.FilterProductView.as_view(), name='filtered_products'),
    
]


