from django.contrib import admin
from .models import ExerciseSession, WeekEntry


class WeekEntryInline(admin.StackedInline):
    model = WeekEntry
    extra = 0


@admin.register(ExerciseSession)
class ExerciseSessionAdmin(admin.ModelAdmin):
    list_display = ("short_name", "name")
    search_fields = ("short_name", "name")
    inlines = [WeekEntryInline]


@admin.register(WeekEntry)
class WeekEntryAdmin(admin.ModelAdmin):
    list_display = (
        "exercise_session",
        "week_number",
        "materials_number",
        "exercise_materials_link",
    )
    list_filter = ("exercise_session", "week_number")
    search_fields = (
        "exercise_session__short_name",
        "exercise_session__name",
        "week_number",
    )
