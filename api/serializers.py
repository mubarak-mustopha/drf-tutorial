from rest_framework import serializers
from storeapp.models import *

from rest_framework.serializers import StringRelatedField


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "category_id",
            "title",
            "slug",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "slug",
            "inventory",
            "old_price",
            "price",
        ]

    category = CategorySerializer()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description", "product"]

    product = serializers.StringRelatedField()

    def create(self, validated_data):
        validated_data["product_id"] = self.context["product_id"]
        return super().create(validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = Cartitems
        fields = ["id", "product", "quantity", "subTotal"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="get_total")

    class Meta:
        model = Cart
        fields = ["cart_id", "items", "total"]

    def get_total(self, cart: Cart):
        return cart.cart_total
