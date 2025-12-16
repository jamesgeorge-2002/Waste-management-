from django.contrib import admin
from .models import Reward, Penalty


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'reason', 'awarded_at')


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'reason', 'issued_at')
