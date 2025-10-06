from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage,  Catagory,  Product, Favorite, Cart, Notification
from .serializers import  OfferSerializer, HeroImageSerializer, ApiSerializer, ProductSerializer, FavoriteSerializer, CartSerializer, NotificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView, LoginView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.generics import ListAPIView

from rest_framework.decorators import action

class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter




class CustomLoginView(LoginView):
    # def get_response(self):
    #     response = super().get_response()
    #     refresh = RefreshToken.for_user(self.user)
    #     response.data['refresh'] = str(refresh)
    #     response.data['role'] = "admin" if self.user.is_staff or self.user.is_superuser else "user"

    #     return 
     def get_response(self):
        # Get the response from the parent class (standard login flow)
        response = super().get_response()

        # Authentication happens here:
        # self.user is set if the login is successful, as it's managed by LoginView
        user = self.user

        # If user is authenticated, generate a JWT refresh token and include role in response
        if user is not None:
            # Generate a refresh token using the authenticated user
            refresh = RefreshToken.for_user(user)
            response.data['refresh'] = str(refresh)
            
            # Determine the user's role based on permissions (e.g., staff or superuser)
            response.data['role'] = "admin" if user.is_staff or user.is_superuser else "user"
        else:
            # Handle the case where the authentication fails (user not found or incorrect credentials)
            response.data['error'] = 'Invalid credentials'
            response.status_code = 401  # Unauthorized status code

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
        catagory = request.data.get('catagory')
        print(catagory)
        queryset = Product.objects.all()

    
        if catagory:
            catagory_obj = get_object_or_404(Catagory, name=catagory)
            queryset = queryset.filter(catagory=catagory_obj)
       

        serializer = ProductSerializer(queryset, many=True)
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
