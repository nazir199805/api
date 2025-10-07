from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage,  category,  Product, Favorite, Cart, Notification, Order
from .serializers import  OfferSerializer, HeroImageSerializer, ApiSerializer, ProductSerializer, FavoriteSerializer, CartSerializer, NotificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView, LoginView
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import action
from taggit.models import Tag 

class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter




class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        response.data['refresh'] = str(refresh)
        response.data['role'] = "admin" if self.user.is_staff or self.user.is_superuser else "user"
        
        return response





class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  



class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  



class ApiViewSet(viewsets.ModelViewSet):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
    permission_classes = [AllowAny]


class OfferViewSet(viewsets.ModelViewSet):
    queryset = offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]

class HeroImageViewSet(viewsets.ModelViewSet):
    queryset = HeroImage.objects.filter(is_active=True).order_by('order')
    serializer_class = HeroImageSerializer
    permission_classes = [AllowAny]



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





class FilterProductView(APIView):
    
    def post(self, request):
        # Get category and tags from the request body
        category_name = request.data.get('category')
        tags = request.data.get('tags', [])
        
        # Start with all products
        queryset = Product.objects.all()

        # Apply category filter if category is provided
        if category_name:
            category = get_object_or_404(category, name=category_name)
            queryset = queryset.filter(category=category)

        # Apply tag filter if tags are provided
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        # Serialize the filtered queryset
        serializer = ProductSerializer(queryset, many=True)

        # Return the filtered products
        return Response(serializer.data, status=status.HTTP_200_OK)







class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter notifications by the current user
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        # Mark a specific notification as read
        try:
            notification = Notification.objects.get(id=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)
        
        notification.is_read = True
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)



class UserOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context