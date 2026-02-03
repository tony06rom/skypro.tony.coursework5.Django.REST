from django.contrib import admin

from .models import Habit, HabitEvent


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "periodicity", "time", "is_public", "is_pleasant")
    list_filter = ("is_public", "is_pleasant", "periodicity", "user")
    list_editable = ("is_public",)
    search_fields = ("name", "user__email", "place")


@admin.register(HabitEvent)
class HabitEventAdmin(admin.ModelAdmin):
    list_display = ("habit", "status", "performed_at")
    list_filter = ("status", "performed_at")
