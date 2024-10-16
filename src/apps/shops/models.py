from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    """Модель магазина"""

    name = models.CharField(
        _('Название'),
        max_length=128,
        unique=True,
    )
    description = models.CharField(
        _('Описание'),
        max_length=1024,
        null=True, blank=True,
    )
    avatar = models.ImageField(
        _('Аватар'),
        upload_to='shops/avatars/',
        null=True, blank=True,
    )
    address = models.CharField(
        _('Адрес'),
        max_length=1024,
        null=True, blank=True,
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='shops', related_query_name='shop',
        verbose_name=_('Владелец'),
    )

    class Meta:
        verbose_name = _('Магазин')
        verbose_name_plural = _('Магазины')

    def __str__(self):
        return self.name
