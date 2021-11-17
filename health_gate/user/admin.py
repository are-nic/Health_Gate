from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    """Кастомная модель Админа с полем номера телефона вместо логина"""

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('full_name',
                                         'nickname',
                                         'email',
                                         'profession',
                                         'address',
                                         'about',
                                         'photo',
                                         'tags',
                                         'twitter',
                                         'facebook',
                                         'instagram',
                                         'youtube',
                                         'patreon',
                                         )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    list_filter = DjangoUserAdmin.list_filter + ('groups__name',)
    list_display = ('phone_number', 'full_name', 'custom_group', 'is_staff', 'is_active')
    search_fields = ('phone_number',)
    ordering = ('phone_number',)

    def custom_group(self, obj):
        """
        получить группы, разделенные запятой и вывести пустую строку если пользователь не имеет группу.
        для вывода групп пользователей в списке пользователей админ панели
        """
        return ','.join([group.name for group in obj.groups.all()]) if obj.groups.count() else ''