from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from .models import CustomUser


@admin.register(CustomUser)
class CartItem(admin.ModelAdmin):
    list_display = ('email', 'is_superuser', 'is_active', 'last_login',)
    ordering = ('-is_superuser', '-is_active',)

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'phone','password'),
            }
        ),
        (
            _('Additionally'),
            {
                'fields': (('first_name', 'last_name', 'middle_name'),
                           'gender', 'avatar', 'birthday', 'address'),
                # 'classes': ('collapse',),
            }
        ),
        (
            _('Control'),
            {
                'fields': (('last_login', 'date_joined'),
                           ('is_superuser', 'is_staff', 'is_active'),
                           ('groups', 'user_permissions')),
            }
        )
    )