from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'price', 'discount',)
    list_display_links = ('name', 'shop',)
    list_editable = ('discount',)
    ordering = ('price',)
    search_fields = ('name', 'shop__name',)