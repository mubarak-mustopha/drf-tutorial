from rest_framework import serializers
from storeapp.models import Product, Category, Review

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
