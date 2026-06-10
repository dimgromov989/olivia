from django.core.validators import (MaxValueValidator,  # <== Здесь импорты
                                    MinValueValidator)
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с полями created_at и updated_at.
    """

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField("Название категории", max_length=100)
    slug = models.SlugField("Слаг (URL)", max_length=100, unique=True, blank=True)

    crm_id = models.CharField(
        "ID в r-keeper (RK7)",
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text="ID группы блюд в кассе. Не менять!",
    )
    image = models.ImageField(
        "Изображение категории", upload_to="menu/categories/", blank=True, null=True
    )
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )
    name = models.CharField("Название товара", max_length=200)
    slug = models.SlugField("Слаг (URL)", max_length=200, unique=True, blank=True)
    description = models.TextField("Описание / Состав", blank=True)

    image = models.ImageField(
        "Изображение товара", upload_to="menu/products/", blank=True, null=True
    )
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2, default=0)
    old_price = models.DecimalField(
        "Старая цена (для скидки)",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Если заполнено, на сайте будет отображаться как зачёркнутая цена",
        default=0,
    )
    crm_id = models.CharField(
        "ID в r-keeper (RK7)",
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        help_text="ID блюда в кассе. Не менять!",
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество", default=0, blank=True, null=False
    )
    weight = models.DecimalField(
        verbose_name="Вес (кг)",
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0.001, message="Вес не может быть меньше 1 г"),
            MaxValueValidator(999.999, message="Вес слишком большой"),
        ],
    )
    is_available = models.BooleanField(
        verbose_name="В наличии?",
        default=True,
        help_text="Отмечайте, если товар можно купить.",
    )
    is_active = models.BooleanField("Отображать в меню", default=True)
    is_out_of_stock = models.BooleanField("Стоп-лист", default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"], name="unique_product_name_in_category"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
