from rest_framework import serializers

from apps.shops.models import Shop
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории продукта"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'description',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели продукта"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'image', 'description',
                  'added_at', 'discount', 'shop', 'categories')

    def validate(self, attrs):
        shop = attrs.get('shop')
        if not shop.owner == self.context['request'].user:
            raise serializers.ValidationError("Вы не можете создавать продукты в этом магазине.")
        return attrs