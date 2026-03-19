from django.contrib import admin
from .models import MenstrualProfile, CycleDay, DailyLog, CycleInsight


@admin.register(MenstrualProfile)
class MenstrualProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_period_start', 'avg_cycle_length', 'pregnancy_goal']
    list_filter = ['pregnancy_goal', 'last_period_start']
    search_fields = ['user__u_phone_number', 'user__first_name']
    fields = ['user', 'last_period_start', 'avg_cycle_length', 'avg_period_length', 'pregnancy_goal']
    readonly_fields = ['user']


@admin.register(CycleDay)
class CycleDayAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'cycle_day_number', 'phase', 'fertility_level']
    list_filter = ['phase', 'fertility_level', 'date']
    search_fields = ['user__u_phone_number']
    readonly_fields = ['user', 'date', 'cycle_day_number', 'phase', 'fertility_level']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'bleeding_level', 'pain_score', 'mood']
    list_filter = ['bleeding_level', 'mood', 'date']
    search_fields = ['user__u_phone_number', 'notes']
    fieldsets = (
        ('User & Date', {'fields': ['user', 'date']}),
        ('Symptoms', {'fields': ['bleeding_level', 'pain_score', 'mood', 'symptoms']}),
        ('Notes', {'fields': ['notes']}),
    )


@admin.register(CycleInsight)
class CycleInsightAdmin(admin.ModelAdmin):
    list_display = ['user', 'insight_type', 'title', 'date']
    list_filter = ['insight_type', 'date']
    search_fields = ['user__u_phone_number', 'title', 'description']
    readonly_fields = ['user', 'date']

