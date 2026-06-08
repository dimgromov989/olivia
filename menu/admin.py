from django.contrib import admin
from .models import Category, Product, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ['name', 'crm_id', 'price', 'is_active']
    verbose_name = "Вариант (размер/модификатор)"
    verbose_name_plural = "Варианты товара"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'crm_id', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'crm_id']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'crm_id', 'is_active', 'is_out_of_stock']
    list_filter = ['category', 'is_active', 'is_out_of_stock']
    search_fields = ['name', 'crm_id', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline] 


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'crm_id', 'price', 'is_active']
    list_filter = ['is_active', 'product__category']
    search_fields = ['name', 'product__name', 'crm_id']
