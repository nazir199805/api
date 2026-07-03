from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'users', views.ApiViewSet)
router.register(r'hero', views.HeroImageViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'favorites', views.FavoriteViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'sections', views.SectionViewSet)


urlpatterns = [
    path("products/search/", views.ProductSearchView.as_view()),
    path("favorites/toggle/", views.ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("carts/add/",views.AddToCartView.as_view()),
    path("carts/remove/<int:item_id>/", views.RemoveCartItemView.as_view()),
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('products/filter', views.FilterProductView.as_view(), name='filtered_products'),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("orders/", views.my_orders),
    path("orders/<int:order_id>/", views.order_detail),
  
]


