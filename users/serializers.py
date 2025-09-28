from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Api, offer, HeroImage, HeroButton


class HeroButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroButton
        fields = ['id', 'text', 'link']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
       user = User.objects.create_user(**validated_data)
       return user





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