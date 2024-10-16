from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    """Модель отзыва"""

    GRADES = (
        (1, 'Ужасно'),
        (2, 'Не очень'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )

    grade = models.PositiveSmallIntegerField(
        _('Оценка'),
        choices=GRADES,
        null=True, blank=True,
    )
    comment = models.CharField(
        _('Комментарий'),
        max_length=1024,
        null=True, blank=True,
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='reviews', related_query_name='review',
        verbose_name=_('Продукт'),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reviews', related_query_name='review',
        verbose_name=_('Покупатель'),
    )
    # created_at
    # updated_at

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')

    def __str__(self):
        return str(self.id)