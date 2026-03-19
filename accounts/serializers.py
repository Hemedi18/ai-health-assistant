from rest_framework import serializers
from .models import (
    User, Profile, HealthVital, MedicalHistory, ChildProfile,
    NutritionEntry, DailyNutritionGoal, WaterIntake,
    Exercise, DailySteps, FitnessGoal,
    MoodEntry, SleepEntry, MindfulnessSession,
    Medication, MedicationReminder, MedicationAdherence, MedicalAppointment,
    BloodSugarEntry, HealthReport
)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['health_focus', 'date_of_birth', 'blood_group']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['u_id', 'u_phone_number', 'is_premium', 'trial_start', 'profile']


# ==================== HEALTH VITALS ====================

class HealthVitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthVital
        fields = ['id', 'weight', 'height', 'blood_pressure_sys', 'blood_pressure_dia', 
                  'heart_rate', 'bmi', 'recorded_at']
        read_only_fields = ['bmi', 'recorded_at']


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['allergies', 'chronic_conditions', 'family_history']


class ChildProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildProfile
        fields = ['id', 'name', 'date_of_birth', 'vaccination_status']


# ==================== NUTRITION ====================

class NutritionEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionEntry
        fields = ['id', 'meal_type', 'food_items', 'calories', 'protein_g', 
                  'carbs_g', 'fat_g', 'fiber_g', 'notes', 'recorded_at']
        read_only_fields = ['recorded_at']


class DailyNutritionGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyNutritionGoal
        fields = ['target_calories', 'target_protein_g', 'target_carbs_g', 
                  'target_fat_g', 'target_fiber_g', 'target_water_ml', 
                  'special_diet', 'last_updated']
        read_only_fields = ['last_updated']


class WaterIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterIntake
        fields = ['id', 'amount_ml', 'recorded_at']
        read_only_fields = ['recorded_at']


# ==================== FITNESS ====================

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'exercise_type', 'intensity', 'duration_minutes', 
                  'calories_burned', 'notes', 'recorded_at']
        read_only_fields = ['recorded_at']


class DailyStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailySteps
        fields = ['id', 'steps', 'distance_km', 'recorded_date']
        read_only_fields = ['recorded_date']


class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessGoal
        fields = ['target_steps_daily', 'target_exercise_minutes_weekly', 
                  'target_workouts_weekly', 'last_updated']
        read_only_fields = ['last_updated']


# ==================== MENTAL HEALTH ====================

class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['id', 'mood', 'triggers', 'anxiety_level', 'stress_level', 
                  'notes', 'recorded_at']
        read_only_fields = ['recorded_at']


class SleepEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepEntry
        fields = ['id', 'sleep_duration_hours', 'sleep_quality', 'bed_time', 
                  'wake_time', 'notes', 'recorded_date']
        read_only_fields = ['recorded_date']


class MindfulnessSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MindfulnessSession
        fields = ['id', 'session_type', 'duration_minutes', 'feeling_before', 
                  'feeling_after', 'recorded_at']
        read_only_fields = ['recorded_at']


# ==================== MEDICATION ====================

class MedicationReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationReminder
        fields = ['id', 'reminder_time', 'is_active']


class MedicationSerializer(serializers.ModelSerializer):
    reminders = MedicationReminderSerializer(many=True, read_only=True)
    
    class Meta:
        model = Medication
        fields = ['id', 'medication_name', 'dosage', 'frequency', 'reason', 
                  'start_date', 'end_date', 'side_effects', 'notes', 'is_active', 
                  'reminders']


class MedicationAdherenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationAdherence
        fields = ['id', 'medication', 'scheduled_date', 'was_taken', 
                  'time_taken', 'skipped_reason']


class MedicalAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalAppointment
        fields = ['id', 'doctor_name', 'clinic_name', 'appointment_date', 
                  'reason', 'notes', 'reminder_sent', 'created_at']
        read_only_fields = ['created_at']


# ==================== BLOOD SUGAR ====================

class BloodSugarEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodSugarEntry
        fields = ['id', 'blood_sugar_mg_dl', 'measurement_time', 'notes', 'recorded_at']
        read_only_fields = ['recorded_at']


# ==================== HEALTH REPORTS ====================

class HealthReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReport
        fields = ['id', 'report_date', 'avg_weight', 'avg_blood_pressure', 
                  'avg_heart_rate', 'avg_blood_sugar', 'total_calories', 
                  'total_exercise_minutes', 'total_steps', 'avg_mood_score', 
                  'avg_sleep_hours', 'health_risks', 'recommendations', 'created_at']
        read_only_fields = ['report_date', 'created_at']