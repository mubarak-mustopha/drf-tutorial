from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)

from .serializers import ProductSerializer, CategorySerializer
from storeapp.models import Product, Category


# Create your views here.
# CBV'S
class ApiProducts(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ApiProduct(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ApiCategorys(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ApiCategory(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

