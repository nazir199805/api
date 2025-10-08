from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage,  Category,  Product, Favorite, Cart, Notification, Order
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

# class GoogleLogin(SocialLoginView): 
#     adapter_class = GoogleOAuth2Adapter

import requests
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model

User = get_user_model()

class GoogleLoginSafe(APIView):
    """
    Receives only the authorization code from frontend,
    exchanges it for access_token and id_token securely,
    then creates or fetches the user.
    """
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Missing authorization code"}, status=status.HTTP_400_BAD_REQUEST)

        # Get Google OAuth credentials from Django SocialApp
        try:
            app = SocialApp.objects.get(provider='google')
        except SocialApp.DoesNotExist:
            return Response({"error": "Google SocialApp not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            "code": code,
            "client_id": app.client_id,
            "client_secret": app.secret,
            "redirect_uri": "http://localhost:5173",  # Must match the frontend redirect
            "grant_type": "authorization_code"
        }

        # Exchange code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_resp = requests.post(token_url, data=data)
        if token_resp.status_code != 200:
            return Response({"error": "Failed to get tokens from Google", "details": token_resp.json()}, status=status.HTTP_400_BAD_REQUEST)

        tokens = token_resp.json()  # contains access_token, id_token, expires_in, etc.
        id_token = tokens.get('id_token')
        access_token = tokens.get('access_token')

        # Optional: validate id_token with Google if needed

        # Optional: get user info
        user_info_resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_resp.status_code != 200:
            return Response({"error": "Failed to fetch user info from Google"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_resp.json()
        email = user_info.get("email")
        if not email:
            return Response({"error": "Google did not return an email"}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get user
        user, created = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0]})

        return Response({
            "user": {"id": user.id, "email": user.email, "username": user.username},
            "access_token": access_token,
            "id_token": id_token
        })



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
            category = get_object_or_404(Category, name=category_name)
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
    



from .models import Product, Order, Notification, Favorite, offer, User








def dashboard_callback(request, context):
    # Fetching data for dashboard stats
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    unread_notifications = Notification.objects.all().count()
    total_favorites = Product.objects.all().count()

    # Fetching recent products (you can adjust the limit as needed)
    recent_products = Product.objects.all()[:5]

    # Offer data (assuming the 'Offer' model contains discount information)
    offer1 = offer.objects.last()  # Fetching the most recent offer

    # Passing data to the template
    context.update({
        'pending_orders': pending_orders,
        'unread_notifications': unread_notifications,
        'total_favorites': total_favorites,
        'recent_products': recent_products,
        'offer': offer,
        'total_products': total_products,  # Any custom variable you want to add
    })
    return context

