from rest_framework import serializers

from .models import Shop


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор для модели магазина"""

    owner = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Shop
        fields = ('id', 'name', 'description', 'avatar',
                  'address', 'created_at', 'owner',)