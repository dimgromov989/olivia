from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import Category, Product
from .serializers import CategorySerializer, MenuSerializer, ProductDetailSerializer


@extend_schema(
    summary="Получить список категорий",
    description="Возвращает все активные категории",
    tags=["Menu"],
)
class CategoryListView(generics.ListAPIView):
    """
    GET /api/menu/categories/

    Возвращает список всех активных категорий меню.
    """

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("sort_order")


@extend_schema(
    summary="Получить всё меню",
    description="Возвращает все активные категории с их товарами и вариантами",
    tags=["Menu"],
)
class MenuListView(generics.ListAPIView):
    """
    GET /api/menu/

    Возвращает полное меню пиццерии: все активные категории
    с их активными товарами и вариантами (размерами).
    """

    serializer_class = MenuSerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by("sort_order")


@extend_schema(
    summary="Получить товар",
    description="Возвращает детали одного товара с его вариантами",
    tags=["Menu"],
    parameters=[
        OpenApiParameter(
            name="slug",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.PATH,
            description="Slug товара (например: pepperoni, margarita)",
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
    lookup_field = "slug"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")
