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


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    subtotal = serializers.SerializerMethodField(method_name="get_subtotal")

    class Meta:
        model = Cartitems
        fields = ["id", "product", "quantity", "subtotal"]

    def get_subtotal(self, cartitem: Cartitems):
        return cartitem.quantity * cartitem.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    class Meta:
        model = Cartitems
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"No product with the given ID {value}")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Cart item quantity cannot be negative")
        return value

    def save(self, **kwargs):
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        cart_id = self.context["cart_id"]

        cartitem, created = Cartitems.objects.get_or_create(
            product_id=product_id, cart_id=cart_id
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
    cart_id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name="get_total")

    class Meta:
        model = Cart
        fields = ["cart_id", "owner", "items", "total"]

    # owner = serializers.StringRelatedField()
    def get_total(self, cart: Cart):
        items = cart.items.all()
        return sum([item.quantity * item.product.price for item in items])
