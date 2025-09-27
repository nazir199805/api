from django.shortcuts import render
from rest_framework import viewsets
from .models import User, offer
from .serializers import UserSerializer, OfferSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = offer.objects.all()
    serializer_class = OfferSerializer