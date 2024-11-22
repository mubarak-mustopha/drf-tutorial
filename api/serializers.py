from rest_framework import serializers
from storeapp.models import *


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
        fields = ["id", "date_created", "product", "description", "name"]

    product = serializers.StringRelatedField()

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "owner"]

    # owner = serializers.StringRelatedField()
