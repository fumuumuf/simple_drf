from django.contrib import admin

# Register your models here.
from accounts.admin import CustomUserAdmin
from accounts.front_users.models import TenantUser


class UserAdmin(CustomUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('front user information', {'fields': ('name', 'kana')}),
    )

    # def __init__(self, *args, **kwargs):
    #     pass
    # # self.fieldsets = (
    # #     ('front user information', {'fields': ('name', 'kana')})
    # # )
    # self.fieldsets
    # super(UserAdmin, self).__init__(*args, **kwargs)


admin.site.register(TenantUser, UserAdmin)
