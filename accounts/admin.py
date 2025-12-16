from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('full_name', 'user_type', 'local_body_type', 'local_body', 'ward', 'phone', 'is_worker')}),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_superuser', 'is_worker')
    list_filter = ('is_worker', 'user_type', 'local_body')
