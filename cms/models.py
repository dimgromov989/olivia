from django.db import models
from menu.models import TimeStampedModel





class PageBlock(TimeStampedModel):
    BLOCK_TYPES = [
        ('BANNER', 'Промо-баннер'),
        ('CATEGORY_GRID', 'Сетка категорий'),
        ('PRODUCT_CAROUSEL', 'Карусель товаров'),
    ]
    
    block_type = models.CharField("Тип блока", max_length=50, choices=BLOCK_TYPES)
    
    payload = models.JSONField(
        "Данные блока (JSON)", 
        default=dict, 
        blank=True,
        help_text="Для BANNER: {'title': '...', 'image_url': '...'} | Для CATEGORY_GRID: {'category_ids': [1, 2]}"
    )
    
    sort_order = models.PositiveIntegerField("Порядок отображения", default=0)
    is_active = models.BooleanField("Активен", default=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = "Блок главной страницы"
        verbose_name_plural = "Блоки главной страницы"

    def __str__(self):
        return f"{self.get_block_type_display()} (Порядок: {self.sort_order})"

