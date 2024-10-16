from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)