from rest_framework import generics
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404

from .models import Category, Product, ProductVariant
from .serializers import (
    CategorySerializer, 
    ProductDetailSerializer,
    ProductVariantDetailSerializer
)


@extend_schema(
    summary="Получить всё меню",
    description="Возвращает все активные категории с их товарами и вариантами",
    tags=['Menu'],
)
class MenuListView(generics.ListAPIView):
    """
    GET /api/menu/
    
    Возвращает полное меню пиццерии: все активные категории 
    с их активными товарами и вариантами (размерами).
    """
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related(
            'products__variants'
        ).order_by('sort_order')


@extend_schema(
    summary="Получить категорию",
    description="Возвращает одну категорию с её товарами",
    tags=['Menu'],
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Slug категории (например: pizza, drinks)',
        ),
    ],
)
class CategoryDetailView(generics.RetrieveAPIView):
    """
    GET /api/menu/categories/<slug>/
    
    Возвращает детали одной категории с её товарами и вариантами.
    """
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related(
            'products__variants'
        )


@extend_schema(
    summary="Получить товар",
    description="Возвращает детали одного товара с его вариантами",
    tags=['Menu'],
    parameters=[
        OpenApiParameter(
            name='slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Slug товара (например: pepperoni, margarita)',
        ),
    ],
)
class ProductDetailView(generics.RetrieveAPIView):
    """
    GET /api/menu/products/<slug>/
    
    Возвращает полную информацию о товаре: описание, категорию, 
    все доступные варианты (размеры) и цены.
    """
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related(
            'category'
        ).prefetch_related('variants')


@extend_schema(
    summary="Получить вариант товара",
    description="Возвращает детали конкретного варианта товара (например, 'Пепперони 30 см')",
    tags=['Menu'],
    parameters=[
        OpenApiParameter(
            name='product_slug',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description='Slug товара (например: pepperoni)',
        ),
        OpenApiParameter(
            name='variant_id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description='ID варианта товара',
        ),
    ],
)
class ProductVariantDetailView(generics.RetrieveAPIView):
    """
    GET /api/menu/products/{product_slug}/variant/{variant_id}/
    
    Возвращает информацию о конкретном варианте товара.
    Проверяет, что вариант принадлежит указанному товару.
    """
    serializer_class = ProductVariantDetailSerializer
    
    def get_object(self):
        product_slug = self.kwargs.get('product_slug')
        variant_id = self.kwargs.get('variant_id')
        
        product = get_object_or_404(Product, slug=product_slug, is_active=True)
        
        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            product=product,
            is_active=True
        )
        
        return variant