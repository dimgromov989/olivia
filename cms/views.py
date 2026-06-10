from rest_framework import generics

from .models import PageBlock
from .serializers import PageBlockSerializer


class PageBlockListView(generics.ListAPIView):
    """
    GET /api/cms/blocks/
    Возвращает все активные блоки главной страницы
    """

    serializer_class = PageBlockSerializer

    def get_queryset(self):
        return PageBlock.objects.filter(is_active=True).order_by("sort_order")
