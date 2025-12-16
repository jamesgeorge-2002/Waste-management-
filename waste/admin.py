from django.contrib import admin
from .models import WasteRecord, Pickup


@admin.register(WasteRecord)
class WasteRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'waste_type', 'entered_weight', 'verified_weight', 'created_at')
    list_filter = ('waste_type',)
    search_fields = ('user__username', 'user__email')


@admin.register(Pickup)
class PickupAdmin(admin.ModelAdmin):
    list_display = ('id', 'waste_record', 'assigned_worker', 'status', 'scheduled_date')
    list_filter = ('status', 'scheduled_date')
    search_fields = ('waste_record__user__username', 'assigned_worker__worker_id')
    actions = ('auto_assign_to_worker',)

    def auto_assign_to_worker(self, request, queryset):
        """Simple admin action: assign pickup to first approved worker in the same ward."""
        assigned = 0
        for pickup in queryset:
            ward = pickup.ward
            if not ward:
                continue
            worker_qs = pickup.ward.local_body.workers_set if hasattr(pickup.ward.local_body, 'workers_set') else None
            # fallback: find approved worker who has the ward in assigned_wards
            from workers.models import WorkerProfile
            wp = WorkerProfile.objects.filter(assigned_wards=ward, approved=True).first()
            if wp:
                pickup.assigned_worker = wp
                pickup.status = 'assigned'
                pickup.save()
                assigned += 1
        self.message_user(request, f"Assigned {assigned} pickups")
    auto_assign_to_worker.short_description = 'Auto assign selected pickups to worker in ward'
