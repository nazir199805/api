from rest_framework import serializers
from .models import Api, offer, HeroImage, HeroButton, Catagory, Profile, Product, ProductImage, Notification
from dj_rest_auth.registration.serializers import RegisterSerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Order, OrderItem


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

    # Profile fields
    
    gender = serializers.CharField(required=False, default='male')
    

    def save(self, request):
        user = super().save(request)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

        # Save profile fields
        profile = user.profile
        profile.gender = self.validated_data.get('gender', 'male')
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




class OfferSerializer(serializers.ModelSerializer):
  class Meta:
    model = offer
    fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ProductImage
        fields = ['image']

class CatagorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ['name']


# class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
#    sub_images = ProductImageSerializer(many=True, read_only=True)
#    catagory = serializers.StringRelatedField()
#    tags = TagListSerializerField()

#    class Meta:
#       model = Product
#       fields = ['id', 'name', 'price', 'color', 'tags', 'is_favorite', 'sub_images', 'catagory']

 

from .models import Product, Favorite, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    sub_images = ProductImageSerializer(many=True, read_only=True)
    catagory = serializers.StringRelatedField()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'color', 'catagory','brand', 'tags', 'is_favorited','sub_images',]

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


class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)  # To show the username of the user who received the notification
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)  # Format the datetime
    is_read = serializers.BooleanField()  # Include is_read field to show if the notification is read

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_username', 'message', 'created_at', 'is_read']
        read_only_fields = ['user', 'created_at']  # Prevent changes to 'user' and 'created_at' from external requests
    
    def update(self, instance, validated_data):
        """Override the update method to handle the 'mark_as_read' logic."""
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
    


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total_amount', 'items']