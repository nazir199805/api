from rest_framework import viewsets, status
from rest_framework.views import APIView
from .models import Api, HeroImage,  Category, Section,  Product, Favorite, Cart, Order, CartItem, OrderItem
from .serializers import HeroImageSerializer,SectionSerializer ,ApiSerializer, ProductSerializer, FavoriteSerializer, CartSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from dj_rest_auth.registration.views import LoginView
from .serializers import OrderSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import RegisterView
import requests
from django.http import JsonResponse
import json
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()


class ProductSearchView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")

        products = Product.objects.filter(
            name__icontains=query
        )

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).first()

        if favorite:
            favorite.delete()
            return Response({
                "favorite": False,
                "message": "Removed from favorites"
            })

        Favorite.objects.create(
            user=request.user,
            product=product
        )

        return Response({
            "favorite": True,
            "message": "Added to favorites"
        })
    

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=404)

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({
            "message": "Added to cart",
            "quantity": item.quantity
        })

class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()

            return Response({"message": "Item removed from cart"})
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found"},
                status=status.HTTP_404_NOT_FOUND)



class RegisterViewEmail(RegisterView):
    def create(self, request, *args, **kwargs):
        email = request.data.get('email', '').lower().strip()

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {"detail": "Email already in use"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Otherwise, proceed with normal registration
        return super().create(request, *args, **kwargs)

    def get_response(self):
        response = super().get_response()
        # You can modify the successful response here if needed
        response.data['detail'] = "User registered successfully"
        return response


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
            "redirect_uri": "https://aboutyouwebsite.vercel.app",
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

        # Exchange code for access token
        token_url = "https://graph.facebook.com/v19.0/oauth/access_token"
        params = {
            "client_id": settings.SOCIAL_AUTH_FACEBOOK_KEY,
            "client_secret": settings.SOCIAL_AUTH_FACEBOOK_SECRET,
            "redirect_uri": "https://aboutyouwebsite.vercel.app/",
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

        # Use access token to fetch user profile
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

        # Get or create Django user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": username, "first_name": first_name, "last_name": last_name}
        )

        if not created:
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        # Create JWT tokens
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
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by("name")
    serializer_class = SectionSerializer


class ApiViewSet(viewsets.ModelViewSet):
    queryset = Api.objects.all()
    serializer_class = ApiSerializer
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





class UserOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    




from .paypal_utils import get_paypal_access_token

from rest_framework.decorators import permission_classes

from decimal import Decimal

import requests

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, Order, OrderItem



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_paypal_order(request):

    # ---------------------------------------------------------
    # 1. Get active cart
    # ---------------------------------------------------------

    cart = get_object_or_404(
        Cart,
        user=request.user,
        is_active=True
    )

    if not cart.items.exists():
        return Response(
            {
                "detail": "Your cart is empty."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ---------------------------------------------------------
    # 2. Calculate cart total
    # ---------------------------------------------------------

    total = Decimal("0.00")

    for item in cart.items.all():
        total += item.product.price * item.quantity

    total = total.quantize(Decimal("0.01"))

    # ---------------------------------------------------------
    # 3. Find existing pending local order
    # ---------------------------------------------------------

    existing_order = (
        Order.objects
        .filter(
            user=request.user,
            status="pending",
        )
        .order_by("-id")
        .first()
    )

    # ---------------------------------------------------------
    # 4. Get PayPal access token
    # ---------------------------------------------------------

    try:
        token = get_paypal_access_token()

    except Exception as e:

        return Response(
            {
                "detail": "Unable to authenticate with PayPal.",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    # ---------------------------------------------------------
    # 5. Try to reuse existing PayPal order
    # ---------------------------------------------------------

    if existing_order and existing_order.paypal_order_id:

        check_url = (
            f"{settings.PAYPAL_BASE_URL}"
            f"/v2/checkout/orders/"
            f"{existing_order.paypal_order_id}"
        )

        try:

            check_response = requests.get(
                check_url,
                headers=headers,
                timeout=30,
            )

            if check_response.ok:

                paypal_existing = check_response.json()

                paypal_status = paypal_existing.get("status")

                # -------------------------------------------------
                # PayPal order is still usable
                # -------------------------------------------------

                if paypal_status == "CREATED":

                    return Response(
                        {
                            **paypal_existing,

                            "local_order_id": existing_order.id,

                            "reused": True,
                        },
                        status=status.HTTP_200_OK
                    )

        except requests.RequestException:
            # If checking the old order fails,
            # we'll create a new PayPal order below.
            pass

    # ---------------------------------------------------------
    # 6. Existing PayPal order isn't usable.
    # Create a NEW PayPal order.
    # ---------------------------------------------------------

    url = (
        f"{settings.PAYPAL_BASE_URL}"
        f"/v2/checkout/orders"
    )

    data = {
        "intent": "CAPTURE",

        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(total),
                }
            }
        ],

        "application_context": {
            "return_url": (
                "https://aboutyouwebsite.vercel.app/"
                "payment-success"
            ),

            "cancel_url": (
                "https://aboutyouwebsite.vercel.app/"
                "cart"
            ),
        },
    }

    try:

        response = requests.post(
            url,
            json=data,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        paypal_data = response.json()

    except requests.RequestException as e:

        return Response(
            {
                "detail": "Unable to create PayPal order.",
                "error": str(e),
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # ---------------------------------------------------------
    # 7. Make sure PayPal returned an ID
    # ---------------------------------------------------------

    paypal_order_id = paypal_data.get("id")

    if not paypal_order_id:

        return Response(
            {
                "detail": "PayPal did not return an order ID.",
                "paypal": paypal_data,
            },
            status=status.HTTP_502_BAD_GATEWAY
        )

    # ---------------------------------------------------------
    # 8. Reuse existing LOCAL order if possible
    # ---------------------------------------------------------

    if existing_order:

        existing_order.total_amount = total
        existing_order.paypal_order_id = paypal_order_id
        existing_order.status = "pending"

        existing_order.save(
            update_fields=[
                "total_amount",
                "paypal_order_id",
                "status",
            ]
        )

        order = existing_order

    # ---------------------------------------------------------
    # 9. Otherwise create a new LOCAL order
    # ---------------------------------------------------------

    else:

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status="pending",
            paypal_order_id=paypal_order_id,
        )

    # ---------------------------------------------------------
    # 10. Return the COMPLETE PayPal response
    # ---------------------------------------------------------

    return Response(
        {
            **paypal_data,

            "local_order_id": order.id,

            "reused": False,
        },
        status=status.HTTP_201_CREATED
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def capture_paypal_order(request):

    # ---------------------------------------------------------
    # 1. Get PayPal order ID from frontend
    # ---------------------------------------------------------

    order_id = request.data.get("orderID")

    if not order_id:

        return Response(
            {
                "detail": "No PayPal order id."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ---------------------------------------------------------
    # 2. Get PayPal access token
    # ---------------------------------------------------------

    try:
        token = get_paypal_access_token()

    except Exception as e:

        return Response(
            {
                "detail": "Unable to authenticate with PayPal.",
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # ---------------------------------------------------------
    # 3. Lock the local order
    #
    # select_for_update() prevents two requests from
    # processing the same Django order simultaneously.
    # ---------------------------------------------------------

    try:

        with transaction.atomic():

            order = (
                Order.objects
                .select_for_update()
                .get(
                    paypal_order_id=order_id,
                    user=request.user,
                )
            )

            # -------------------------------------------------
            # 4. Prevent double processing
            # -------------------------------------------------

            if order.status == "paid":

                return Response(
                    {
                        "message": "Order already processed.",
                        "order_id": order.id,
                        "status": "paid",
                    },
                    status=status.HTTP_200_OK,
                )

            # -------------------------------------------------
            # 5. Make sure order is still pending
            # -------------------------------------------------

            if order.status != "pending":

                return Response(
                    {
                        "detail": (
                            f"Order cannot be captured because "
                            f"its current status is "
                            f"'{order.status}'."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # -------------------------------------------------
            # 6. Capture PayPal order
            # -------------------------------------------------

            url = (
                f"{settings.PAYPAL_BASE_URL}"
                f"/v2/checkout/orders/{order_id}/capture"
            )

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }

            try:

                paypal_response = requests.post(
                    url,
                    headers=headers,
                    timeout=30,
                )

            except requests.RequestException as e:

                return Response(
                    {
                        "detail": "Unable to contact PayPal.",
                        "error": str(e),
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # -------------------------------------------------
            # 7. Parse PayPal response
            # -------------------------------------------------

            try:
                paypal_data = paypal_response.json()

            except ValueError:

                return Response(
                    {
                        "detail": "Invalid response received from PayPal."
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            # -------------------------------------------------
            # 8. Check PayPal HTTP response
            # -------------------------------------------------

            if not paypal_response.ok:

                return Response(
                    {
                        "detail": "PayPal capture failed.",
                        "paypal": paypal_data,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # -------------------------------------------------
            # 9. IMPORTANT:
            # Verify PayPal says payment is COMPLETED
            # -------------------------------------------------

            paypal_status = paypal_data.get("status")

            if paypal_status != "COMPLETED":

                return Response(
                    {
                        "detail": "PayPal payment was not completed.",
                        "paypal_status": paypal_status,
                        "paypal": paypal_data,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # -------------------------------------------------
            # 10. Get actual PayPal capture ID
            # -------------------------------------------------

            capture_id = None

            purchase_units = paypal_data.get(
                "purchase_units",
                []
            )

            if purchase_units:

                payments = (
                    purchase_units[0]
                    .get("payments", {})
                )

                captures = payments.get(
                    "captures",
                    []
                )

                if captures:

                    capture_id = captures[0].get("id")

            # -------------------------------------------------
            # 11. Fallback
            # -------------------------------------------------

            if not capture_id:

                capture_id = paypal_data.get("id")

            # -------------------------------------------------
            # 12. Get user's active cart
            # -------------------------------------------------

            cart = get_object_or_404(
                Cart,
                user=request.user,
                is_active=True,
            )

            # Make sure cart isn't empty
            if not cart.items.exists():

                return Response(
                    {
                        "detail": (
                            "Payment completed, but the "
                            "cart is empty."
                        ),
                        "order_id": order.id,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # -------------------------------------------------
            # 13. Prevent duplicate OrderItems
            # -------------------------------------------------

            if not order.items.exists():

                for item in cart.items.all():

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )

            # -------------------------------------------------
            # 14. Mark order as paid
            # -------------------------------------------------

            order.status = "paid"

            order.paypal_capture_id = capture_id

            order.transaction_id = capture_id

            order.save(
                update_fields=[
                    "status",
                    "paypal_capture_id",
                    "transaction_id",
                ]
            )

            # -------------------------------------------------
            # 15. Clear cart
            # -------------------------------------------------

            cart.items.all().delete()

            cart.is_active = False

            cart.save(
                update_fields=[
                    "is_active"
                ]
            )

            # -------------------------------------------------
            # 16. Return success
            # -------------------------------------------------

            return Response(
                {
                    "message": "Payment successful.",

                    "order_id": order.id,

                    "paypal_order_id": order.paypal_order_id,

                    "paypal_capture_id": capture_id,

                    "status": order.status,

                    "paypal": paypal_data,
                },
                status=status.HTTP_200_OK,
            )

    except Order.DoesNotExist:

        return Response(
            {
                "detail": (
                    "PayPal order was not found or "
                    "does not belong to this user."
                )
            },
            status=status.HTTP_404_NOT_FOUND,
        )





from .models import Product, Order, Favorite, User


def dashboard_callback(request,context):
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

    ]
    recent_products = Product.objects.all().order_by('-id')[:5]  # adjust field if needed

    # Build table data
    table_data = {
        "headers": ["Name", "Price", "Brand", "Category"],
        "rows": [
            [p.name, f"${p.price}", p.brand, p.category]
            for p in recent_products
        ]
    }

    # update the incoming context and return it (no render)
    context.update({"cards": cards,
                    "table_data":table_data,
                })
    return context


class ContactView(APIView):
    permission_classes = []

    def post(self, request):
        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        message = request.data.get("message")

        email_body = f"""
New Contact Message

Name: {full_name}
Email: {email}
Phone: {phone}

Message:
{message}
"""

        send_mail(
            subject=f"Contact Form - {full_name}",
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["nazirsherzad12345@gmail.com"],
        )

        return Response(
            {"detail": "Message sent successfully."},
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


@csrf_exempt
def paypal_webhook(request):

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    if data.get("event_type") == "PAYMENT.CAPTURE.COMPLETED":

        resource = data.get("resource", {})

        order_id = (
            resource.get("supplementary_data", {})
            .get("related_ids", {})
            .get("order_id")
        )

        capture_id = resource.get("id")

        if not order_id:
            return JsonResponse({"error": "no order id"}, status=400)

        try:
            order = Order.objects.get(paypal_order_id=order_id)

            # prevent double updates
            if order.status != "paid":
                order.status = "paid"
                order.paypal_capture_id = capture_id
                order.save()

            print("ORDER PAID:", order.id)

            return JsonResponse({"status": "updated"})

        except Order.DoesNotExist:
            return JsonResponse({"error": "order not found"}, status=404)

    return JsonResponse({"status": "ignored"})