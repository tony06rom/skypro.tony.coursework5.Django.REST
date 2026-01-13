from django.contrib import admin
from .models import Habit, HabitEvent


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "period_type", "frequency", "time", "is_public")
    list_filter = ("period_type", "is_public", "is_pleasant")


@admin.register(HabitEvent)
class HabitEventAdmin(admin.ModelAdmin):
    list_display = ("habit", "status", "performed_at")
    list_filter = ("status", "performed_at")
