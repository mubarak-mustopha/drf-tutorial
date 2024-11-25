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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "inventory",
            "old_price",
            "price",
            "images",
            "uploaded_images",
        ]

    # category = CategorySerializer()
    category = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        uploaded_images = validated_data["uploaded_images"]
        print(f"**\n{uploaded_images}\n**")
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            print(f"**\n{image}\n**")
            ProductImage.objects.create(product=product, image=image)
        return product


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
