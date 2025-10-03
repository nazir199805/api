from rest_framework import serializers
from .models import Api, offer, HeroImage, HeroButton, Product, ProductImage, Catagory
from dj_rest_auth.registration.serializers import RegisterSerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from dj_rest_auth.serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()
        return user



class HeroButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroButton
        fields = ['id', 'text', 'link']



class HeroImageSerializer(serializers.ModelSerializer):
    buttons = HeroButtonSerializer(many=True, read_only=True)  # nested data

    class Meta:
        model = HeroImage
        fields = ['id', 'image', 'title', 'description', 'order', 'is_active', 'buttons']




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


class ProductSerializer(TaggitSerializer, serializers.ModelSerializer):
   sub_images = ProductImageSerializer(many=True, read_only=True)
   catagory = serializers.StringRelatedField()
   tags = TagListSerializerField()

   class Meta:
      model = Product
      fields = ['id', 'name', 'price', 'color', 'tags', 'is_favorite', 'main_image', 'sub_images', 'catagory']