from rest_framework import serializers
from .models import PageBlock

class PageBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageBlock
        fields = ['id', 'block_type', 'payload', 'sort_order']