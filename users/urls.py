from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', views.ApiViewSet)
router.register(r'offers', views.OfferViewSet)
router.register(r'hero', views.HeroImageViewSet)
router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # path('user/register', views.CreateUserView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    # path('api-auth', include("rest_framework.urls")),
    path('auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/products/filter', views.FilterProductView.as_view(), name='filtered_products'),
    
]


