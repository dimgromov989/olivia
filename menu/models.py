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
    
    crm_id = models.CharField("ID в r-keeper (RK7)", max_length=50, unique=True, null=True, blank=True, db_index=True, help_text="ID группы блюд в кассе. Не менять!")
    image = models.ImageField("Изображение категории", upload_to='menu/categories/', blank=True, null=True)
    sort_order = models.PositiveIntegerField("Порядок сортировки", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = "Категория меню"
        verbose_name_plural = "Категории меню"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Категория")
    name = models.CharField("Название товара", max_length=200)
    slug = models.SlugField("Слаг (URL)", max_length=200, unique=True, blank=True)
    description = models.TextField("Описание / Состав", blank=True)
    
    image = models.ImageField("Изображение товара", upload_to='menu/products/', blank=True, null=True)
    
    crm_id = models.CharField("ID в r-keeper (RK7)", max_length=50, unique=True, null=True, blank=True, db_index=True, help_text="ID блюда в кассе. Не менять!")
    
    is_active = models.BooleanField("Отображать в меню", default=True)
    is_out_of_stock = models.BooleanField("Стоп-лист", default=False)

    class Meta:
        ordering = ['name']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        constraints = [models.UniqueConstraint(fields=['category', 'name'], name='unique_product_name_in_category')]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def min_price(self):
        min_variant = self.variants.filter(is_active=True).order_by('price').first()
        return float(min_variant.price) if min_variant else 0.0


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name="Товар")
    name = models.CharField("Название варианта", max_length=100, help_text="Например: '30 см', '40 см'")
    
    crm_id = models.CharField("ID варианта в r-keeper", max_length=50, null=True, blank=True, db_index=True, help_text="ID модификатора в RK7")
    
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    is_active = models.BooleanField("Доступен для заказа", default=True)

    class Meta:
        verbose_name = "Вариант товара"
        verbose_name_plural = "Варианты товаров"

    def __str__(self):
        return f"{self.product.name} — {self.name} ({self.price} ₽)"