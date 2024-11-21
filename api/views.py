from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .filters import ProductFilterSet
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from storeapp.models import Product, Category, Review


# Create your views here.
# MODELVIEWSETS
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["category", "top_deal"]
    filterset_class = ProductFilterSet
    search_fields = ["name", "description"]
    ordering_fields = ["old_price"]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return super().get_queryset()


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        print(f"{'*'*5}{self.kwargs}{'*'*5}")
        return Review.objects.filter(product=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


# CBV'S
class ProductsAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        print(self.kwargs)
        print(self.request.query_params)
        return super().get_queryset()
