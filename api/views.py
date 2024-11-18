from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import ProductSerializer, CategorySerializer
from storeapp.models import Product, Category


# Create your views here.
# CBV'S
class ApiProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ApiProduct(APIView):

    def delete(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ApiCategorys(APIView):
    def get(self, request):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ApiCategory(APIView):

    def delete(self, request, pk):
        cat = get_object_or_404(Category, category_id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk):
        cat = get_object_or_404(Category, category_id=pk)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    def put(self, request, pk):
        cat = get_object_or_404(Category, category_id=pk)

        serializer = CategorySerializer(cat, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# FBV'S
@api_view(["GET", "POST"])
def api_categorys(request):
    if request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
    data = serializer.data
    return Response(data)


@api_view(["GET", "PUT", "DELETE"])
def api_category(request, pk):
    cat = get_object_or_404(Category, category_id=pk)

    if request.method == "DELETE":
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = CategorySerializer(cat, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    else:
        serializer = CategorySerializer(cat)
    data = serializer.data
    return Response(data)
