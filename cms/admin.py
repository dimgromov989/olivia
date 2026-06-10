from django import forms
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.utils.html import format_html

from .forms import BLOCK_FORMS
from .models import PageBlock


class PageBlockAdminForm(forms.ModelForm):
    """Базовая форма с выбором типа блока"""

    class Meta:
        model = PageBlock
        fields = ["block_type", "sort_order", "is_active"]


@admin.register(PageBlock)
class PageBlockAdmin(admin.ModelAdmin):
    list_display = [
        "block_type",
        "sort_order",
        "is_active",
        "created_at",
        "preview_link",
    ]
    list_editable = ["sort_order", "is_active"]
    list_filter = ["block_type", "is_active"]
    ordering = ["sort_order"]

    def get_form(self, request, obj=None, **kwargs):
        """Возвращаем нужную форму в зависимости от типа блока"""
        if request.method == "POST" and "block_type" in request.POST:
            block_type = request.POST.get("block_type")
            if block_type in BLOCK_FORMS:
                return BLOCK_FORMS[block_type]

        if obj and obj.block_type in BLOCK_FORMS:
            return BLOCK_FORMS[obj.block_type]

        return PageBlockAdminForm

    def get_fieldsets(self, request, obj=None):
        """Настраиваем отображение полей в зависимости от типа блока"""
        if obj and obj.block_type == "BANNER":
            return [
                ("Основное", {"fields": ("block_type", "sort_order", "is_active")}),
                (
                    "Содержимое баннера",
                    {
                        "fields": (
                            "title",
                            "subtitle",
                            "image",
                            "button_text",
                            "button_link",
                        ),
                        "description": "Заполните данные для промо-баннера",
                    },
                ),
            ]
        elif obj and obj.block_type == "CATEGORY_GRID":
            return [
                ("Основное", {"fields": ("block_type", "sort_order", "is_active")}),
                (
                    "Сетка категорий",
                    {
                        "fields": ("title", "category_ids"),
                        "description": "Укажите ID категорий через запятую. "
                        "Например: 1,2,3 (где 1=Пицца, 2=Напитки)",
                    },
                ),
            ]
        elif obj and obj.block_type == "PRODUCT_CAROUSEL":
            return [
                ("Основное", {"fields": ("block_type", "sort_order", "is_active")}),
                (
                    "Карусель товаров",
                    {
                        "fields": ("title", "product_slugs"),
                        "description": "Укажите slug товаров через запятую. "
                        "Например: pepperoni,margarita,four-cheese",
                    },
                ),
            ]

        return super().get_fieldsets(request, obj)

    class Media:
        css = {"all": ()}
        js = ()

    def get_urls(self):
        """Добавляем кастомный URL для предпросмотра"""
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:object_id>/preview/",
                self.admin_site.admin_view(self.preview_view),
                name="cms_pageblock_preview",
            ),
        ]
        return custom_urls + urls

    def preview_view(self, request, object_id):
        """View для предпросмотра блока"""
        block = PageBlock.objects.get(pk=object_id)
        return render(
            request,
            "admin/cms/pageblock_preview.html",
            {
                "block": block,
                "opts": self.model._meta,
            },
        )

    def preview_link(self, obj):
        """Ссылка на предпросмотр в списке блоков"""
        if obj.pk:
            return format_html(
                '<a href="/admin/cms/pageblock/{}/preview/" target="_blank" '
                'style="color: #417690; font-weight: bold;">Просмотр</a>',
                obj.pk,
            )
        return "—"

    preview_link.short_description = "Предпросмотр"
