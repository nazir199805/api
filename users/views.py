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
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
import requests
from dj_rest_auth.jwt_auth import set_jwt_access_cookie, set_jwt_refresh_cookie

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView): 
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'postmessage'
    client_class = OAuth2Client





class GoogleCodeExchangeView(APIView):
    def post(self, request):
        code = request.data.get('code')
        print(f"code: {code}")

        if not code:
            return Response({"detail": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        url = "https://tashya-mendez.onrender.com/auth/google/"

        try:
            google_res = requests.post(url, json={'code': code})
        except Exception as e:
            return Response({"detail": f"Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if google_res.status_code == status.HTTP_200_OK:
            data = google_res.json()
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            if not access_token or not refresh_token:
                return Response({"detail": "Missing tokens from response"}, status=status.HTTP_400_BAD_REQUEST)

            res = Response(
                {"detail": "Able to get the tokens"},
                status=status.HTTP_200_OK
            )

            set_jwt_access_cookie(res, access_token)
            set_jwt_refresh_cookie(res, refresh_token)

            return res
        else:
            return Response(
                {
                    "detail": "Failed to exchange code",
                    "status_code": google_res.status_code,
                    "response": google_res.text,
                },
                status=google_res.status_code
            )




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

