from rest_framework import serializers

from .models import CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели элемента корзины"""

    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'user', 'product')


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для модели элемента заказа"""

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity', 'total_amount')


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели заказа"""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'total_amount',
                  'dispatch_date', 'arrival_date', 'from_field', 'to', 'items')
