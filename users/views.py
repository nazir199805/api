from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Api, offer, HeroImage,  Category,  Product, Favorite, Cart, Notification, Order
from .serializers import  OfferSerializer, HeroImageSerializer, ApiSerializer, ProductSerializer, FavoriteSerializer, CartSerializer, NotificationSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from dj_rest_auth.registration.views import SocialLoginView, LoginView
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import action
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
import requests
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
User = get_user_model()





#Login with Google View
class GoogleCodeExchangeView(LoginView, APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        if not code:
            return Response({"detail": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange code with Google
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "http://localhost:3000",
            "grant_type": "authorization_code",
        }

        try:
            google_res = requests.post(token_url, data=payload)
            google_res.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": f"Google token exchange failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token_data = google_res.json()
        id_token_str = token_data.get("id_token")
        if not id_token_str:
            return Response({"detail": "Missing ID token from Google response"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verify Google ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            return Response({"detail": "Invalid ID token"}, status=status.HTTP_400_BAD_REQUEST)

        email_str = idinfo.get("email")
        first_name = idinfo.get("given_name", "")   # Google first name
        last_name = idinfo.get("family_name", "")   # Google last name
        username = email_str.split('@')[0]

        # Get or create the user
        user, created = User.objects.get_or_create(
            email=email_str,
            defaults={"username": username, "first_name": first_name, "last_name": last_name}
        )

        # Optional: update name if user already exists
        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()


        # Generate JWT tokens like in CustomLoginView
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response_data = {
        "access": access,
        "refresh": str(refresh),
        "user": {
            "pk": user.pk,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        },
        "role": "admin" if user.is_staff or user.is_superuser else "user"
}


        return Response(response_data, status=status.HTTP_200_OK)
    


# Login wuth Facebook View
class FacebookLogin(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if not code:
            return Response({"detail": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 1️⃣ Exchange code for access token
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        params = {
            "client_id": settings.SOCIAL_AUTH_FACEBOOK_KEY,
            "client_secret": settings.SOCIAL_AUTH_FACEBOOK_SECRET,
            "redirect_uri": "https://localhost:3000/",
            "code": code,
        }

        try:
            token_res = requests.get(token_url, params=params)
            token_res.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": f"Facebook token exchange failed: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token_data = token_res.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response({"detail": "No access token returned from Facebook"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 2️⃣ Use access token to fetch user profile
        user_info_url = "https://graph.facebook.com/me"
        user_params = {
            "fields": "id,name,email,first_name,last_name",
            "access_token": access_token,
        }

        try:
            user_info_res = requests.get(user_info_url, params=user_params)
            user_info_res.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": f"Failed to fetch Facebook user info: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_info = user_info_res.json()
        email = user_info.get("email")
        if not email:
            return Response({"detail": "Facebook account has no email permission granted"},
                            status=status.HTTP_400_BAD_REQUEST)

        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        username = email.split("@")[0]

        # 3️⃣ Get or create Django user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": username, "first_name": first_name, "last_name": last_name}
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        # 4️⃣ Create JWT tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response_data = {
            "access": access,
            "refresh": str(refresh),
            "user": {
                "pk": user.pk,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "role": "admin" if user.is_staff or user.is_superuser else "user"
        }

        return Response(response_data, status=status.HTTP_200_OK)










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
    """
    Unfold expects us to receive a context dict, update it and return it.
    Don't call render() here.
    """
    cards = [
         {
            "title": "Hero Section",
            "metric": HeroImage.objects.all().count(),
            "link": "admin:users_heroimage_changelist",
            "icon": "image",
        },
        {
            "title": "Products",
            "metric": Product.objects.count(),
            "link": "admin:users_product_changelist",   # named admin url -- keep as string
            "icon": "shopping_bag",
        },
        {
            "title": "Orders",
            "metric": Order.objects.count(),
            "link": "admin:users_order_changelist",
            "icon": "package",
        },
        {
            "title": "Users",
            "metric": User.objects.count(),
            "link": "admin:auth_user_changelist",
            "icon": "person",
        },
        {
            "title": "Favorites",
            "metric": Favorite.objects.count(),
            "link": "admin:users_favorite_changelist",
            "icon": "favorite",
        },
        {
            "title": "Unread Notifications",
            "metric": Notification.objects.filter(is_read=False).count(),
            "link": "admin:users_notification_changelist",
            "icon": "notifications",
        },
       
    ]
    recent_products = Product.objects.all()[:5]  # adjust field if needed

    # Build table data
    table_data = {
        "headers": ["Name", "Price", "Brand", "Category", "Color"],
        "rows": [
            [p.name, f"${p.price}", p.brand, p.category, p.color]
            for p in recent_products
        ]
    }

    # update the incoming context and return it (no render)
    context.update({"cards": cards,
                    "table_data":table_data,
                })
    return context
