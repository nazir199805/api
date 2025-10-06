from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage,  Catagory,  Product
from .serializers import  OfferSerializer, HeroImageSerializer, ApiSerializer, ProductSerializer
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


class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        response.data['refresh'] = str(refresh)
        response.data['role'] = "admin" if self.user.is_staff or self.user.is_superuser else "user"
        return response





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
