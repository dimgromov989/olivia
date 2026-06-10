from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "crm_id", "sort_order", "is_active", "image"]
    list_editable = ["sort_order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "crm_id"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "old_price",
        "quantity",
        "weight",
        "is_available",
        "is_out_of_stock",
        "is_active",
    ]
    list_filter = ["category", "is_active", "is_available", "is_out_of_stock"]
    search_fields = ["name", "crm_id", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["is_available", "is_active", "is_out_of_stock"]
    list_per_page = 20
