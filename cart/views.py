# cart/views.py
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from .utils import get_or_create_cart


@extend_schema_view(
    list=extend_schema(
        summary="Получить корзину",
        description="Возвращает текущую корзину пользователя или гостя со всеми товарами и итоговой суммой.",
        responses={
            200: OpenApiResponse(
                response=CartSerializer, description="Корзина успешно получена"
            )
        },
        tags=["Корзина"],
    ),
    clear=extend_schema(
        summary="Очистить корзину",
        description="Полностью удаляет все товары из корзины.",
        responses={
            204: OpenApiResponse(description="Корзина успешно очищена"),
        },
        tags=["Корзина"],
    ),
)
class CartViewSet(viewsets.GenericViewSet):
    """
    Управление корзиной.
    """

    permission_classes = [AllowAny]
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        cart = get_or_create_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return Response(
            {"detail": "Корзина очищена"}, status=status.HTTP_204_NO_CONTENT
        )


@extend_schema_view(
    create=extend_schema(
        summary="Добавить товар в корзину",
        description="Добавляет товар в корзину. По умолчанию добавляется 1 штука, "
        "но можно указать нужное количество в поле `quantity`. "
        "Если товар уже есть в корзине, его количество увеличивается.",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "integer",
                        "description": "ID продукта",
                        "example": 5,
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Количество (по умолчанию 1)",
                        "example": 1,
                        "default": 1,
                        "minimum": 1,
                    },
                },
                "required": ["product"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=CartItemSerializer,
                description="Товар успешно добавлен",
            ),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["Товары в корзине"],
    ),
    destroy=extend_schema(
        summary="Удалить товар из корзины",
        description="Удаляет одну единицу товара из корзины. "
        "Если передать параметр `?all=true`, удалятся все единицы этого товара.",
        parameters=[
            OpenApiParameter(
                name="all",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Если true, удаляет все единицы товара (по умолчанию false)",
                default=False,
            )
        ],
        responses={
            204: OpenApiResponse(description="Товар успешно удален"),
            403: OpenApiResponse(description="Нельзя удалять товары из чужой корзины"),
            404: OpenApiResponse(description="Товар не найден в корзине"),
        },
        tags=["Товары в корзине"],
    ),
)
class CartItemViewSet(viewsets.GenericViewSet):
    """
    Управление товарами в корзине.
    """

    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart = get_or_create_cart(self.request)
        return CartItem.objects.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        current_cart = get_or_create_cart(request)
        if instance.cart != current_cart:
            raise PermissionDenied("Нельзя удалять товары из чужой корзины")
        remove_all = request.query_params.get("all", "false").lower() == "true"

        if remove_all:
            instance.delete()
        else:
            if instance.quantity > 1:
                instance.quantity -= 1
                instance.save()
            else:
                instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
