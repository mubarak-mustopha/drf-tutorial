from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import ProductSerializer, CategorySerializer
from storeapp.models import Product, Category


# Create your views here.
@api_view()
def api_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    data = serializer.data
    print(data)
    return Response(data)


@api_view()
def api_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    data = ProductSerializer(product).data
    return Response(data)


@api_view()
def api_categorys(request):
    cats = Category.objects.all()
    data = CategorySerializer(cats, many=True).data
    return Response(data)


@api_view()
def api_category(request, pk):
    cat = get_object_or_404(Category, category_id=pk)
    data = CategorySerializer(cat).data
    return Response(data)
