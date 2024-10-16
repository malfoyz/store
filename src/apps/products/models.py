from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Модель категории продукта"""

    name = models.CharField(
        _('Название'),
        max_length=64,
        unique=True,
    )
    description = models.CharField(
        _('Описание'),
        max_length=1024,
        null=True, blank=True,
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(
        _('Название'),
        max_length=64,
        db_index=True,
    )
    price = models.DecimalField(
        _('Цена'),
        max_digits=10, decimal_places=2,
        validators=(validators.MinValueValidator(0),),
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='products/',
        null=True, blank=True,
    )
    description = models.CharField(
        _('Описание'),
        max_length=1024,
        null=True, blank=True,
    )
    added_at = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
    )
    discount = models.PositiveSmallIntegerField(
        _('Скидка %'),
        default=0,
        validators=(validators.MaxValueValidator(100),)
    )
    shop = models.ForeignKey(
        'shops.Shop',
        on_delete=models.PROTECT,
        related_name='products', related_query_name='product',
        verbose_name=_('Магазин'),
    )
    categories = models.ManyToManyField(
        Category,
        related_name='categories', related_query_name='category',
        blank=True,
        verbose_name=_('Категории'),
    )

    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')
        constraints = (models.UniqueConstraint(fields=('name', 'shop'),
                                               name='product_in_shop_unique_constraint'),)

    def __str__(self):
        return f'{self.name} ({self.shop.name})'