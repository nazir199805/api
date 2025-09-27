from rest_framework import serializers
from .models import User, offer

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
  class Meta:
    model = offer
    fields = '__all__'