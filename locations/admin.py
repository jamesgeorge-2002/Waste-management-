from django.contrib import admin
from .models import LocalBody, Ward


@admin.register(LocalBody)
class LocalBodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'body_type')


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'local_body')
    list_filter = ('local_body',)
