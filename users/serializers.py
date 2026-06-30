from rest_framework import serializers
from .models import Api, HeroImage, HeroButton,Section, Category, Profile, Product, ProductImage
from dj_rest_auth.registration.serializers import RegisterSerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order, OrderItem
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_name', 'created_at']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            "id",
            "name",
            "description",
            "image",
            "is_active",
            "filter_by",  
        ]

class CustomLoginSerializer(LoginSerializer):
    username = None
    def validate(self, attrs):
        data = super().validate(attrs)

        
        refresh = RefreshToken.for_user(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data





class CustomRegisterSerializer(RegisterSerializer):
    username = None  
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    email = serializers.EmailField(required=True)


    

    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

        # Save profile fields
        profile = user.profile
        profile.save()

        return user








class HeroButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroButton
        fields = ['id', 'text', 'link']



class HeroImageSerializer(serializers.ModelSerializer):
    buttons = HeroButtonSerializer(many=True, read_only=True)  # nested data

    class Meta:
        model = HeroImage
        fields = ['id', 'image', 'title', 'order', 'is_active', 'buttons']




class ApiSerializer(serializers.ModelSerializer):
  class Meta:
    model = Api
    fields = '__all__'





class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ProductImage
        fields = ['image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


# class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
#    sub_images = ProductImageSerializer(many=True, read_only=True)
#    category = serializers.StringRelatedField()
#    tags = TagListSerializerField()

#    class Meta:
#       model = Product
#       fields = ['id', 'name', 'price', 'color', 'tags', 'is_favorite', 'sub_images', 'category']

 

from .models import Product, Favorite, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    sub_images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category','brand', 'tags', 'is_favorited','sub_images',]

    def get_is_favorited(self, obj):
        user = self.context.get('user')  
        if user and Favorite.objects.filter(user=user, product=obj).exists():
            return True
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'product_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_name', 'product_price', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'user_username', 'is_active', 'items']
        read_only_fields = ['user']

    

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total_amount', 'items']



from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.forms import user_pk_to_url_str


def frontend_url_generator(request, user, temp_key):
    uid = user_pk_to_url_str(user)

    return (
        f"{settings.FRONTEND_URL}"
        f"/reset-password/{uid}/{temp_key}/"
    )


class CustomPasswordResetSerializer(PasswordResetSerializer):
    print("🔥 CUSTOM PASSWORD RESET SERIALIZER IS RUNNING")
    def get_email_options(self):
        return {
            "url_generator": frontend_url_generator,
        }