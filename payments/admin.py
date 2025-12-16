from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'amount', 'paid')
    list_filter = ('paid', 'month')
    search_fields = ('user__username', 'invoice_number')
