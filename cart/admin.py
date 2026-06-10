from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Inline для отображения товаров прямо в странице корзины.
    TabularInline - табличный вид (компактный).
    Можно заменить на StackedInline, если хочешь блочный вид.
    """

    model = CartItem
    extra = 0
    readonly_fields = ("total_price",)
    fields = ("product", "quantity", "total_price")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Админка для модели корзины.
    """

    list_display = (
        "id",
        "user",
        "session_id_short",
        "items_count",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "user__is_active",
    )
    search_fields = (
        "user__email",
        "user__username",
        "session_id",
    )
    readonly_fields = (
        "total_price",
        "created_at",
        "updated_at",
    )
    inlines = [CartItemInline]
    ordering = ("-updated_at",)
    date_hierarchy = "updated_at"

    def session_id_short(self, obj):
        """Показываем сокращенный session_id для гостей"""
        if obj.session_id:
            return f"{str(obj.session_id)[:8]}..."
        return "—"

    session_id_short.short_description = "Session ID"

    def items_count(self, obj):
        """Количество товаров в корзине"""
        count = obj.items.count()
        total_qty = sum(item.quantity for item in obj.items.all())
        return f"{count} поз. ({total_qty} шт.)"

    items_count.short_description = "Товары"

    def total_price(self, obj):
        """Итоговая сумма корзины"""
        return f"{obj.total_price} ₽"

    total_price.short_description = "Сумма"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Админка для отдельного просмотра позиций корзины.
    """

    list_display = (
        "id",
        "cart",
        "product",
        "quantity",
        "total_price",
    )
    list_filter = (
        "product",
        "cart__user",
    )
    search_fields = (
        "product__name",
        "cart__user__email",
    )
    readonly_fields = ("total_price",)
    ordering = ("-id",)

    def total_price(self, obj):
        return f"{obj.total_price} ₽"

    total_price.short_description = "Сумма позиции"
