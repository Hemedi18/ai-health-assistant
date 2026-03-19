from django.contrib import admin
from django.utils.html import format_html
from .models import (
    User, Profile, HealthVital, MedicalHistory, ChildProfile,
    NutritionEntry, DailyNutritionGoal, WaterIntake,
    Exercise, DailySteps, FitnessGoal,
    MoodEntry, SleepEntry, MindfulnessSession,
    Medication, MedicationReminder, MedicationAdherence, MedicalAppointment,
    BloodSugarEntry, HealthReport
)


# Customize Admin Site
admin.site.site_header = "Afya Yako AI Admin"
admin.site.site_title = "Afya Yako Admin Panel"
admin.site.index_title = "Welcome to Afya Yako AI Administration"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['u_phone_number', 'is_premium', 'is_active', 'date_joined', 'user_status']
    list_filter = ['is_premium', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['u_phone_number']
    readonly_fields = ['date_joined', 'trial_start']
    
    fieldsets = (
        ('Account Information', {
            'fields': ('u_phone_number', 'password')
        }),
        ('Status', {
            'fields': ('is_premium', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'trial_start'),
            'classes': ('collapse',)
        }),
    )
    
    def user_status(self, obj):
        """Display user status with color indicators"""
        if obj.is_superuser:
            return format_html('<span style="color: red; font-weight: bold;">⭐ Admin</span>')
        elif obj.is_premium:
            return format_html('<span style="color: gold; font-weight: bold;">💎 Premium</span>')
        else:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
    user_status.short_description = 'Status'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'health_focus', 'blood_group']
    list_filter = ['health_focus']
    search_fields = ['user__u_phone_number']
    readonly_fields = ['user']


@admin.register(HealthVital)
class HealthVitalAdmin(admin.ModelAdmin):
    list_display = ['user', 'weight', 'blood_pressure_display', 'heart_rate', 'recorded_at']
    list_filter = ['recorded_at', 'user']
    search_fields = ['user__u_phone_number']
    readonly_fields = ['recorded_at']
    date_hierarchy = 'recorded_at'
    
    def blood_pressure_display(self, obj):
        sys = obj.blood_pressure_sys or '-'
        dia = obj.blood_pressure_dia or '-'
        return f"{sys}/{dia}"
    blood_pressure_display.short_description = "Blood Pressure"


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__u_phone_number']


@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'date_of_birth']
    search_fields = ['name', 'parent__u_phone_number']


@admin.register(NutritionEntry)
class NutritionEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'meal_type', 'calories', 'recorded_at']
    list_filter = ['meal_type', 'recorded_at']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_at'


@admin.register(DailyNutritionGoal)
class DailyNutritionGoalAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__u_phone_number']


@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount_ml', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_at'


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise_type', 'intensity']
    list_filter = ['exercise_type', 'intensity']
    search_fields = ['user__u_phone_number']


@admin.register(DailySteps)
class DailyStepsAdmin(admin.ModelAdmin):
    list_display = ['user', 'steps', 'recorded_date']
    list_filter = ['recorded_date']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_date'


@admin.register(FitnessGoal)
class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_steps_daily', 'target_exercise_minutes_weekly']
    search_fields = ['user__u_phone_number']


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'stress_level', 'recorded_at']
    list_filter = ['mood', 'recorded_at']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_at'


@admin.register(SleepEntry)
class SleepEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'sleep_duration_hours', 'sleep_quality', 'recorded_date']
    list_filter = ['sleep_quality', 'recorded_date']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_date'


@admin.register(MindfulnessSession)
class MindfulnessSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'duration_minutes', 'recorded_at']
    list_filter = ['session_type', 'recorded_at']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_at'


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__u_phone_number']


@admin.register(MedicationReminder)
class MedicationReminderAdmin(admin.ModelAdmin):
    list_display = ['medication', 'reminder_time']
    search_fields = ['medication__user__u_phone_number']


@admin.register(MedicationAdherence)
class MedicationAdherenceAdmin(admin.ModelAdmin):
    list_display = ['medication', 'scheduled_date', 'was_taken']
    list_filter = ['was_taken', 'scheduled_date']
    search_fields = ['medication__user__u_phone_number']
    date_hierarchy = 'scheduled_date'


@admin.register(MedicalAppointment)
class MedicalAppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor_name', 'appointment_date']
    list_filter = ['appointment_date']
    search_fields = ['user__u_phone_number', 'doctor_name']
    date_hierarchy = 'appointment_date'


@admin.register(BloodSugarEntry)
class BloodSugarEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_sugar_mg_dl', 'recorded_at']
    list_filter = ['measurement_time', 'recorded_at']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'recorded_at'


@admin.register(HealthReport)
class HealthReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'report_date', 'avg_blood_pressure']
    list_filter = ['report_date']
    search_fields = ['user__u_phone_number']
    date_hierarchy = 'report_date'

