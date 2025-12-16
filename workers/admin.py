from django.contrib import admin
from .models import WorkerProfile


@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('worker_id', 'user', 'local_body', 'approved')
    list_filter = ('approved', 'local_body')
    search_fields = ('worker_id', 'user__username', 'user__email', 'user__first_name', 'user__last_name')
