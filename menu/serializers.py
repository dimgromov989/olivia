from rest_framework import serializers
from .models import Category, Product, ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    """Сериализатор для вариантов товара (размеры)"""
    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'crm_id', 'price', 'is_active']


class ProductVariantDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для одного варианта товара"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    category_name = serializers.CharField(source='product.category.name', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'name', 'crm_id', 'price', 'is_active',
            'product_name', 'product_slug', 'category_name', 'image'
        ]
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.product.image and request:
            return request.build_absolute_uri(obj.product.image.url)
        return None


class CategoryBriefSerializer(serializers.ModelSerializer):
    """Краткая информация о категории (без списка товаров)"""
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'sort_order']
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров (используется внутри категории)"""
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    min_price = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category', 'category_name',
            'image', 'min_price', 'is_active', 'is_out_of_stock', 'variants'
        ]
    
    def get_min_price(self, obj):
        return obj.min_price
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий (с товарами внутри) — для списка меню"""
    products = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'sort_order', 'products']
    
    def get_products(self, obj):
        active_products = obj.products.filter(is_active=True)
        return ProductSerializer(
            active_products, 
            many=True, 
            context=self.context
        ).data
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для одного товара"""
    category = CategoryBriefSerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'category',
            'image', 'is_active', 'is_out_of_stock', 'variants',
            'created_at', 'updated_at'
        ]
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None