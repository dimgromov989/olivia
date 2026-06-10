from rest_framework import serializers

from .models import Category, Product


class CategoryBriefSerializer(serializers.ModelSerializer):
    """Краткая информация о категории (без списка товаров)"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "sort_order"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров (используется внутри категории)"""

    category_name = serializers.CharField(source="category.name", read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category_name",
            "image",
            "description",
            "weight",
            "is_available",
            "price",
            "old_price",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий — для списка меню"""

    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "products"]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для одного товара"""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "crm_id",
            "slug",
            "image",
            "description",
            "is_active",
            "quantity",
            "weight",
            "is_available",
            "price",
            "old_price",
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
