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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=100000,
            allow_empty_file=True,
            use_url=True,
        ),
        allow_empty=True,
        required=False,
        write_only=True,
    )

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
            "images",
            "uploaded_images",
        ]

    category = serializers.StringRelatedField()

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", [])
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product


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


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    class Meta:
        model = Cartitems
        fields = ["product_id", "quantity"]

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"No product with the given ID {value}")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Can't pass a negative value as quantity")
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        cartitem, created = Cartitems.objects.get_or_create(
            cart_id=cart_id, product_id=product_id
        )
        if created:
            cartitem.quantity = quantity
        else:
            cartitem.quantity += quantity
        cartitem.save()
        self.instance = cartitem
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartitems
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="get_total")

    class Meta:
        model = Cart
        fields = ["cart_id", "owner", "items", "total"]

    def get_total(self, cart: Cart):
        return cart.cart_total
