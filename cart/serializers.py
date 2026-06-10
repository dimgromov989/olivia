from rest_framework import serializers

from .models import Cart, CartItem
from .utils import get_or_create_cart


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    product_image_url = serializers.SerializerMethodField()

    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image_url",
            "quantity",
            "total_price",
        ]

    def get_product_image_url(self, obj):
        """
        Безопасно получаем URL картинки.
        Если картинки нет - возвращаем None.
        """
        if obj.product.image and hasattr(obj.product.image, "url"):
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.product.image.url)
            return obj.product.image.url
        return None

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value

    def create(self, validated_data):
        cart = get_or_create_cart(self.context["request"])
        product = validated_data["product"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": validated_data.get("quantity", 1)},
        )

        if not created:
            cart_item.quantity += validated_data.get("quantity", 1)
            cart_item.save()

        return cart_item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ["id", "session_id", "items", "total_price"]
