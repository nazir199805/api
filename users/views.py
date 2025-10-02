from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage, Product
from .serializers import  OfferSerializer, HeroImageSerializer, ApiSerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework import status
from rest_framework.response import Response


class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter




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
        category = request.data.get('category')
       
        queryset = Product.objects.all()

    
        if category:
            queryset = queryset.filter(category=category)
       

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
