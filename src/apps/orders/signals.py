from typing import Any, Dict

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import OrderItem


@receiver(post_save, sender=OrderItem)
def order_item_saved_handler(
        sender: type(OrderItem),
        instance: OrderItem,
        **kwargs: Dict[str, Any],
) -> None:
    """
    Обработчик, вызываемый при сохранении записи OrderItem.

    Обновляет общую стоимость заказа после добавления или изменения элемента заказа.
    """
    instance.order.calculate_total_amount()


@receiver(post_delete, sender=OrderItem)
def order_item_deleted_handler(
        sender: type(OrderItem),
        instance: OrderItem,
        **kwargs: Dict[str, Any],
) -> None:
    """
    Обработчик, вызываемый при удалении записи OrderItem.

    Обновляет общую стоимость заказа после удаления элемента заказа.
    """
    instance.order.calculate_total_amount()