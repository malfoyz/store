from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CartItem, Order, OrderItem


@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'user', 'added_at', )
    list_editable = ('quantity',)
    search_fields = ('user__email',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'dispatch_date', 'arrival_date',)
    list_display_links = ('id', 'customer',)
    list_editable = ('status', 'arrival_date',)
    ordering = ('status', 'dispatch_date',)
    list_filter = ('status',)

    readonly_fields = ('dispatch_date', 'total_amount',)

    fieldsets = (
        (
            None,
            {
                'fields': ('status', 'customer', 'total_amount',),
            }
        ),
        (
            _('Delivery info'),
            {
                'fields':  ('dispatch_date', 'arrival_date', 'from_field', 'to',),
            }
        ),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'total_amount')
    ordering = ('total_amount',)

    readonly_fields = ('total_amount',)

