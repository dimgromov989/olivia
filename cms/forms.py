from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import PageBlock


class BannerBlockForm(forms.ModelForm):
    """Форма для промо-баннера с загрузкой изображения"""

    title = forms.CharField(
        label="Заголовок",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "vLargeTextField"}),
    )
    subtitle = forms.CharField(
        label="Подзаголовок",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
    )
    image = forms.ImageField(
        label="Изображение баннера",
        required=False,
        help_text="Загрузите изображение баннера (рекомендуемый размер: 1920x600)",
    )
    button_text = forms.CharField(label="Текст кнопки", max_length=50, required=False)
    button_link = forms.CharField(
        label="Ссылка кнопки",
        max_length=500,
        required=False,
        help_text="Например: /menu/#pizza",
    )

    class Meta:
        model = PageBlock
        fields = ["block_type", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.payload:
            self.fields["title"].initial = self.instance.payload.get("title", "")
            self.fields["subtitle"].initial = self.instance.payload.get("subtitle", "")
            self.fields["button_text"].initial = self.instance.payload.get(
                "button_text", ""
            )
            self.fields["button_link"].initial = self.instance.payload.get(
                "button_link", ""
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        payload = {
            "title": self.cleaned_data["title"],
            "subtitle": self.cleaned_data.get("subtitle", ""),
            "button_text": self.cleaned_data.get("button_text", ""),
            "button_link": self.cleaned_data.get("button_link", ""),
        }

        image = self.cleaned_data.get("image")
        if image:
            filename = f"cms/banners/{image.name}"
            file_path = default_storage.save(filename, ContentFile(image.read()))
            image_url = default_storage.url(file_path)
            payload["image_url"] = image_url
        else:
            payload["image_url"] = (
                self.instance.payload.get("image_url", "") if self.instance.pk else ""
            )

        instance.payload = payload

        if commit:
            instance.save()
        return instance


class CategoryGridBlockForm(forms.ModelForm):
    """Форма для сетки категорий"""

    title = forms.CharField(
        label="Заголовок секции", max_length=200, required=False, initial="Наше меню"
    )
    category_ids = forms.CharField(
        label="Категории",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите ID категорий через запятую (например: 1,2,3)",
                "class": "vTextField",
            }
        ),
        help_text="ID категорий из таблицы menu_category (через запятую)",
    )

    class Meta:
        model = PageBlock
        fields = ["block_type", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.payload:
            self.fields["title"].initial = self.instance.payload.get(
                "title", "Наше меню"
            )
            category_ids = self.instance.payload.get("category_ids", [])
            self.fields["category_ids"].initial = ",".join(map(str, category_ids))

    def save(self, commit=True):
        instance = super().save(commit=False)
        category_ids_str = self.cleaned_data["category_ids"]
        category_ids = [
            int(x.strip()) for x in category_ids_str.split(",") if x.strip().isdigit()
        ]

        instance.payload = {
            "title": self.cleaned_data["title"],
            "category_ids": category_ids,
        }
        if commit:
            instance.save()
        return instance


class ProductCarouselBlockForm(forms.ModelForm):
    """Форма для карусели товаров"""

    title = forms.CharField(
        label="Заголовок секции", max_length=200, required=False, initial="Хиты продаж"
    )
    product_slugs = forms.CharField(
        label="Товары",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите slug товаров через запятую (например: pepperoni,margarita)",
                "class": "vTextField",
            }
        ),
        help_text="Slug товаров из таблицы menu_product (через запятую)",
    )

    class Meta:
        model = PageBlock
        fields = ["block_type", "sort_order", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.payload:
            self.fields["title"].initial = self.instance.payload.get(
                "title", "Хиты продаж"
            )
            product_slugs = self.instance.payload.get("product_slugs", [])
            self.fields["product_slugs"].initial = ",".join(product_slugs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        product_slugs_str = self.cleaned_data["product_slugs"]
        product_slugs = [x.strip() for x in product_slugs_str.split(",") if x.strip()]

        instance.payload = {
            "title": self.cleaned_data["title"],
            "product_slugs": product_slugs,
        }
        if commit:
            instance.save()
        return instance


BLOCK_FORMS = {
    "BANNER": BannerBlockForm,
    "CATEGORY_GRID": CategoryGridBlockForm,
    "PRODUCT_CAROUSEL": ProductCarouselBlockForm,
}
