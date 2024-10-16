from decimal import Decimal

from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from apps.products.models import Product


class CartItem(models.Model):
    """Модель элемента корзины пользователя"""

    quantity = models.PositiveSmallIntegerField(
        _('Количество'),
        default=1,
    )
    added_at = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items', related_query_name='cart_item',
        verbose_name=_('Пользователь'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_items', related_query_name='cart_item',
        verbose_name=_('Продукт'),
    )

    class Meta:
        verbose_name = _('Элемент корзины')
        verbose_name_plural = _('Элементы корзины')
        constraints = (models.UniqueConstraint(
            fields=('product', 'user'),
            name='cart_item_product_for_user_unique_constraint'),)

    def __str__(self):
        return f'{self.user.id}: {self.product.name} x {self.quantity}'


class Order(models.Model):
    """Модель заказа"""

    STATUSES = (
        ('pending', 'Ожидает обработки'),
        ('processing', 'Принят в обработку'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отгружен'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
        ('returned', 'Возвращен')
    )

    dispatch_date = models.DateField(
        _('Дата отправления'),
        auto_now_add=True,
        editable=True,
    )
    arrival_date = models.DateField(
        _('Дата прибытия'),
        null=True, blank=True,
    )
    from_field = models.CharField(
        _('Адрес отправления'),
        max_length=1024,
        null=True, blank=True,
        db_column='from',
    )
    to = models.CharField(
        _('Адрес прибытия'),
        max_length=1024,
        null=True, blank=True,
    )
    status = models.CharField(
        _('Статус'),
        max_length=10,
        choices=STATUSES,
        default='pending',
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='orders', related_query_name='order',
        verbose_name=_('Заказчик'),
    )
    total_amount = models.DecimalField(
        _('Общая цена'),
        max_digits=10, decimal_places=2,
        default=0.0,
        validators=(validators.MinValueValidator(0),)
    )

    def calculate_total_amount(self):
        self.total_amount = self.items.aggregate(Sum('total_amount'))['total_amount__sum']
        self.save(update_fields=['total_amount'])

    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """Модель элемента заказа"""

    quantity = models.PositiveSmallIntegerField(
        _('Количество'),
        default=1,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items', related_query_name='item',
        verbose_name=_('Заказ'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items', related_query_name='order_item',
        verbose_name=_('Продукт'),
    )
    total_amount = models.DecimalField(
        _('Общая цена'),
        max_digits=10, decimal_places=2,
        default=0.0,
        validators=(validators.MinValueValidator(0),)
    )

    def save(self, *args, **kwargs):
        product = Product.objects.get(id=self.product_id)  # для оптимизации запроса
        self.total_amount = product.price * Decimal(1 - product.discount / 100) * self.quantity
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = _('Элемент заказа')
        verbose_name_plural = _('Элементы заказа')

    def __str__(self):
        return str(self.id)

