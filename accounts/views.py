from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from datetime import timedelta
from django.db.models import Avg, Sum, Count
import json

from .models import (
    User, Profile, HealthVital, MedicalHistory, ChildProfile,
    NutritionEntry, DailyNutritionGoal, WaterIntake,
    Exercise, DailySteps, FitnessGoal,
    MoodEntry, SleepEntry, MindfulnessSession,
    Medication, MedicationReminder, MedicationAdherence, MedicalAppointment,
    BloodSugarEntry, HealthReport
)

from .serializers import (
    UserSerializer, HealthVitalSerializer, NutritionEntrySerializer,
    DailyNutritionGoalSerializer, WaterIntakeSerializer, ExerciseSerializer,
    DailyStepsSerializer, FitnessGoalSerializer, MoodEntrySerializer,
    SleepEntrySerializer, MindfulnessSessionSerializer, MedicationSerializer,
    MedicalAppointmentSerializer, BloodSugarEntrySerializer, HealthReportSerializer,
    MedicationAdherenceSerializer
)

from .forms import (
    HealthVitalForm, NutritionEntryForm, ExerciseForm, 
    MoodEntryForm, SleepEntryForm, MedicationForm
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ==================== HEALTH VITALS ====================

class HealthVitalViewSet(viewsets.ModelViewSet):
    serializer_class = HealthVitalSerializer
    
    def get_queryset(self):
        user = self.request.user
        return HealthVital.objects.filter(user=user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest vital signs"""
        vital = HealthVital.objects.filter(user=request.user).latest('recorded_at')
        serializer = self.get_serializer(vital)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def weekly_average(self, request):
        """Get average vitals for the past week"""
        week_ago = timezone.now() - timedelta(days=7)
        vitals = HealthVital.objects.filter(
            user=request.user,
            recorded_at__gte=week_ago
        )
        
        avg_weight = vitals.aggregate(Avg('weight'))['weight__avg']
        avg_systolic = vitals.aggregate(Avg('blood_pressure_sys'))['blood_pressure_sys__avg']
        avg_diastolic = vitals.aggregate(Avg('blood_pressure_dia'))['blood_pressure_dia__avg']
        avg_heart_rate = vitals.aggregate(Avg('heart_rate'))['heart_rate__avg']
        
        return Response({
            'avg_weight': round(avg_weight, 2) if avg_weight else None,
            'avg_blood_pressure': f"{round(avg_systolic) if avg_systolic else 0}/{round(avg_diastolic) if avg_diastolic else 0}",
            'avg_heart_rate': round(avg_heart_rate) if avg_heart_rate else None,
            'period': 'Last 7 days'
        })


# ==================== NUTRITION ====================

class NutritionEntryViewSet(viewsets.ModelViewSet):
    serializer_class = NutritionEntrySerializer
    
    def get_queryset(self):
        user = self.request.user
        return NutritionEntry.objects.filter(user=user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def today_summary(self, request):
        """Get today's nutrition summary"""
        today = timezone.now().date()
        entries = NutritionEntry.objects.filter(
            user=request.user,
            recorded_at__date=today
        )
        
        total_calories = entries.aggregate(Sum('calories'))['calories__sum'] or 0
        total_protein = entries.aggregate(Sum('protein_g'))['protein_g__sum'] or 0
        total_carbs = entries.aggregate(Sum('carbs_g'))['carbs_g__sum'] or 0
        total_fat = entries.aggregate(Sum('fat_g'))['fat_g__sum'] or 0
        
        goal = DailyNutritionGoal.objects.filter(user=request.user).first()
        target_calories = goal.target_calories if goal else 2000
        
        return Response({
            'total_calories': total_calories,
            'target_calories': target_calories,
            'remaining_calories': max(0, target_calories - total_calories),
            'total_protein_g': round(total_protein, 1),
            'total_carbs_g': round(total_carbs, 1),
            'total_fat_g': round(total_fat, 1),
            'meal_count': entries.count()
        })


class DailyNutritionGoalViewSet(viewsets.ViewSet):
    """Get or update nutrition goals"""
    
    @action(detail=False, methods=['get'])
    def retrieve(self, request):
        goal, _ = DailyNutritionGoal.objects.get_or_create(user=request.user)
        serializer = DailyNutritionGoalSerializer(goal)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update(self, request):
        goal, _ = DailyNutritionGoal.objects.get_or_create(user=request.user)
        serializer = DailyNutritionGoalSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WaterIntakeViewSet(viewsets.ModelViewSet):
    serializer_class = WaterIntakeSerializer
    
    def get_queryset(self):
        return WaterIntake.objects.filter(user=self.request.user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def today_total(self, request):
        """Get today's water intake"""
        today = timezone.now().date()
        total = WaterIntake.objects.filter(
            user=request.user,
            recorded_at__date=today
        ).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
        
        goal = DailyNutritionGoal.objects.filter(user=request.user).first()
        target = goal.target_water_ml if goal else 2000
        
        return Response({
            'total_ml': total,
            'target_ml': target,
            'percentage': round((total / target * 100), 1) if target > 0 else 0
        })


# ==================== FITNESS ====================

class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    
    def get_queryset(self):
        return Exercise.objects.filter(user=self.request.user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def weekly_summary(self, request):
        """Get weekly exercise summary"""
        week_ago = timezone.now() - timedelta(days=7)
        exercises = Exercise.objects.filter(
            user=request.user,
            recorded_at__gte=week_ago
        )
        
        total_minutes = exercises.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        total_calories = exercises.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
        exercise_count = exercises.count()
        
        return Response({
            'total_minutes': total_minutes,
            'total_calories_burned': total_calories,
            'exercise_count': exercise_count,
            'average_duration': round(total_minutes / exercise_count, 1) if exercise_count > 0 else 0
        })


class DailyStepsViewSet(viewsets.ModelViewSet):
    serializer_class = DailyStepsSerializer
    
    def get_queryset(self):
        return DailySteps.objects.filter(user=self.request.user).order_by('-recorded_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FitnessGoalViewSet(viewsets.ViewSet):
    """Get or update fitness goals"""
    
    @action(detail=False, methods=['get'])
    def retrieve(self, request):
        goal, _ = FitnessGoal.objects.get_or_create(user=request.user)
        serializer = FitnessGoalSerializer(goal)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update(self, request):
        goal, _ = FitnessGoal.objects.get_or_create(user=request.user)
        serializer = FitnessGoalSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==================== MENTAL HEALTH ====================

class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    
    def get_queryset(self):
        return MoodEntry.objects.filter(user=self.request.user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def weekly_trends(self, request):
        """Get mood trends for the past week"""
        week_ago = timezone.now() - timedelta(days=7)
        moods = MoodEntry.objects.filter(
            user=request.user,
            recorded_at__gte=week_ago
        ).order_by('recorded_at')
        
        mood_values = {'EXCELLENT': 5, 'GOOD': 4, 'NEUTRAL': 3, 'POOR': 2, 'VERY_POOR': 1}
        mood_scores = [mood_values.get(m.mood, 0) for m in moods]
        avg_score = sum(mood_scores) / len(mood_scores) if mood_scores else 0
        
        return Response({
            'entries': MoodEntrySerializer(moods, many=True).data,
            'average_score': round(avg_score, 1),
            'trend': 'improving' if len(mood_scores) > 1 and mood_scores[-1] > mood_scores[0] else 'declining'
        })


class SleepEntryViewSet(viewsets.ModelViewSet):
    serializer_class = SleepEntrySerializer
    
    def get_queryset(self):
        return SleepEntry.objects.filter(user=self.request.user).order_by('-recorded_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def weekly_average(self, request):
        """Get average sleep for the past week"""
        week_ago = timezone.now().date() - timedelta(days=7)
        entries = SleepEntry.objects.filter(
            user=request.user,
            recorded_date__gte=week_ago
        )
        
        avg_duration = entries.aggregate(Avg('sleep_duration_hours'))['sleep_duration_hours__avg']
        avg_quality = entries.aggregate(Avg('sleep_quality'))['sleep_quality__avg']
        
        return Response({
            'average_duration_hours': round(avg_duration, 1) if avg_duration else 0,
            'average_quality': round(avg_quality, 1) if avg_quality else 0,
            'entries_count': entries.count()
        })


class MindfulnessSessionViewSet(viewsets.ModelViewSet):
    serializer_class = MindfulnessSessionSerializer
    
    def get_queryset(self):
        return MindfulnessSession.objects.filter(user=self.request.user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def monthly_stats(self, request):
        """Get monthly mindfulness statistics"""
        month_ago = timezone.now() - timedelta(days=30)
        sessions = MindfulnessSession.objects.filter(
            user=request.user,
            recorded_at__gte=month_ago
        )
        
        total_minutes = sessions.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        
        return Response({
            'total_sessions': sessions.count(),
            'total_minutes': total_minutes,
            'average_duration': round(total_minutes / sessions.count(), 1) if sessions.count() > 0 else 0
        })


# ==================== MEDICATION ====================

class MedicationViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationSerializer
    
    def get_queryset(self):
        return Medication.objects.filter(user=self.request.user).order_by('-start_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active medications"""
        meds = Medication.objects.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(meds, many=True)
        return Response(serializer.data)


class MedicationAdherenceViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationAdherenceSerializer
    
    def get_queryset(self):
        return MedicationAdherence.objects.filter(medication__user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def adherence_rate(self, request):
        """Get medication adherence rate"""
        month_ago = timezone.now().date() - timedelta(days=30)
        adherence = MedicationAdherence.objects.filter(
            medication__user=request.user,
            scheduled_date__gte=month_ago
        )
        
        taken = adherence.filter(was_taken=True).count()
        total = adherence.count()
        rate = (taken / total * 100) if total > 0 else 0
        
        return Response({
            'taken': taken,
            'total': total,
            'adherence_rate': round(rate, 1)
        })


class MedicalAppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalAppointmentSerializer
    
    def get_queryset(self):
        return MedicalAppointment.objects.filter(user=self.request.user).order_by('appointment_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        upcoming = MedicalAppointment.objects.filter(
            user=request.user,
            appointment_date__gte=timezone.now()
        ).order_by('appointment_date')
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


# ==================== BLOOD SUGAR ====================

class BloodSugarEntryViewSet(viewsets.ModelViewSet):
    serializer_class = BloodSugarEntrySerializer
    
    def get_queryset(self):
        return BloodSugarEntry.objects.filter(user=self.request.user).order_by('-recorded_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def weekly_average(self, request):
        """Get average blood sugar for the past week"""
        week_ago = timezone.now() - timedelta(days=7)
        entries = BloodSugarEntry.objects.filter(
            user=request.user,
            recorded_at__gte=week_ago
        )
        
        avg_sugar = entries.aggregate(Avg('blood_sugar_mg_dl'))['blood_sugar_mg_dl__avg']
        
        return Response({
            'average_mg_dl': round(avg_sugar, 1) if avg_sugar else None,
            'entries_count': entries.count(),
            'status': 'normal' if avg_sugar and 70 <= avg_sugar <= 130 else 'requires_attention'
        })


# ==================== HEALTH REPORTS ====================

class HealthReportViewSet(viewsets.ModelViewSet):
    serializer_class = HealthReportSerializer
    
    def get_queryset(self):
        return HealthReport.objects.filter(user=self.request.user).order_by('-report_date')
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new health report"""
        user = request.user
        week_ago = timezone.now() - timedelta(days=7)
        
        # Collect data
        vitals = HealthVital.objects.filter(user=user, recorded_at__gte=week_ago)
        avg_weight = vitals.aggregate(Avg('weight'))['weight__avg']
        avg_systolic = vitals.aggregate(Avg('blood_pressure_sys'))['blood_pressure_sys__avg']
        avg_diastolic = vitals.aggregate(Avg('blood_pressure_dia'))['blood_pressure_dia__avg']
        avg_heart_rate = vitals.aggregate(Avg('heart_rate'))['heart_rate__avg']
        
        nutrition = NutritionEntry.objects.filter(user=user, recorded_at__gte=week_ago)
        total_calories = nutrition.aggregate(Sum('calories'))['calories__sum'] or 0
        
        exercises = Exercise.objects.filter(user=user, recorded_at__gte=week_ago)
        total_exercise_minutes = exercises.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        
        steps = DailySteps.objects.filter(user=user, recorded_date__gte=week_ago.date())
        total_steps = steps.aggregate(Sum('steps'))['steps__sum'] or 0
        
        moods = MoodEntry.objects.filter(user=user, recorded_at__gte=week_ago)
        mood_values = {'EXCELLENT': 5, 'GOOD': 4, 'NEUTRAL': 3, 'POOR': 2, 'VERY_POOR': 1}
        mood_scores = [mood_values.get(m.mood, 0) for m in moods]
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else 0
        
        sleeps = SleepEntry.objects.filter(user=user, recorded_date__gte=week_ago.date())
        avg_sleep = sleeps.aggregate(Avg('sleep_duration_hours'))['sleep_duration_hours__avg']
        
        # Identify risks
        risks = []
        if avg_systolic and avg_systolic > 140:
            risks.append('high_blood_pressure')
        if total_exercise_minutes < 60:
            risks.append('low_activity')
        if avg_mood and avg_mood < 2.5:
            risks.append('low_mood')
        if avg_sleep and avg_sleep < 6:
            risks.append('insufficient_sleep')
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risks, user)
        
        report = HealthReport.objects.create(
            user=user,
            avg_weight=avg_weight,
            avg_blood_pressure=f"{round(avg_systolic) if avg_systolic else 0}/{round(avg_diastolic) if avg_diastolic else 0}",
            avg_heart_rate=round(avg_heart_rate) if avg_heart_rate else None,
            total_calories=total_calories,
            total_exercise_minutes=total_exercise_minutes,
            total_steps=total_steps,
            avg_mood_score=round(avg_mood, 1),
            avg_sleep_hours=round(avg_sleep, 1) if avg_sleep else None,
            health_risks=json.dumps(risks),
            recommendations=json.dumps(recommendations)
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)
    
    def _generate_recommendations(self, risks, user):
        """Generate health recommendations based on risks"""
        recommendations = []
        
        if 'high_blood_pressure' in risks:
            recommendations.append({
                'category': 'Blood Pressure',
                'message': 'Your blood pressure is elevated. Consider reducing sodium intake, exercising regularly, and managing stress.',
                'priority': 'high'
            })
        
        if 'low_activity' in risks:
            recommendations.append({
                'category': 'Physical Activity',
                'message': 'You need more physical activity. Aim for at least 150 minutes of moderate exercise per week.',
                'priority': 'high'
            })
        
        if 'low_mood' in risks:
            recommendations.append({
                'category': 'Mental Health',
                'message': 'Your mood scores are low. Consider mindfulness activities, talking to someone, or consulting a mental health professional.',
                'priority': 'high'
            })
        
        if 'insufficient_sleep' in risks:
            recommendations.append({
                'category': 'Sleep',
                'message': 'You are not getting enough sleep. Aim for 7-9 hours per night and maintain a consistent sleep schedule.',
                'priority': 'high'
            })
        
        if not risks:
            recommendations.append({
                'category': 'General',
                'message': 'Great job! Keep up your healthy habits and continue monitoring your health.',
                'priority': 'low'
            })
        
        return recommendations


def dashboard_view(request):
    """Main health dashboard view"""
    user = request.user if request.user.is_authenticated else User.objects.first()
    today = timezone.now().date()
    
    # Get today's water intake
    today_water = WaterIntake.objects.filter(user=user, recorded_at__date=today).aggregate(total=models.Sum('amount_ml'))['total'] or 0
    
    # Get today's steps
    today_steps = DailySteps.objects.filter(user=user, recorded_date=today).first()
    
    # --- Graph Data Preparation ---
    # Get last 10 records for the graph
    recent_vitals = HealthVital.objects.filter(user=user).order_by('-recorded_at')[:10]
    
    dates = []
    weights = []
    bp_sys = []
    bp_dia = []
    
    # Reverse to show chronological order (oldest to newest)
    for v in reversed(list(recent_vitals)):
        dates.append(v.recorded_at.strftime("%d/%m"))
        weights.append(float(v.weight) if v.weight else None)
        bp_sys.append(v.blood_pressure_sys)
        bp_dia.append(v.blood_pressure_dia)

    context = {
        'user': user,
        'latest_vital': HealthVital.objects.filter(user=user).latest('recorded_at') if HealthVital.objects.filter(user=user).exists() else None,
        'today_mood': MoodEntry.objects.filter(user=user, recorded_at__date=today).first() if MoodEntry.objects.filter(user=user).exists() else None,
        'today_sleep': SleepEntry.objects.filter(user=user, recorded_date=today).first() if SleepEntry.objects.filter(user=user).exists() else None,
        'today_water': today_water,
        'today_steps': today_steps,
        # Pass graph data as JSON
        'graph_dates': json.dumps(dates),
        'graph_weights': json.dumps(weights),
        'graph_sys': json.dumps(bp_sys),
        'graph_dia': json.dumps(bp_dia),
    }
    
    return render(request, 'accounts/dashboard.html', context)


# ==================== FORM VIEWS (Non-API) ====================

@login_required
def add_vital_view(request):
    if request.method == 'POST':
        form = HealthVitalForm(request.POST)
        if form.is_valid():
            vital = form.save(commit=False)
            vital.user = request.user
            vital.save()
            messages.success(request, 'Vitals recorded successfully!')
            return redirect('dashboard')
    else:
        form = HealthVitalForm()
    return render(request, 'accounts/vitals_form.html', {'form': form, 'title': 'Record Vitals'})

@login_required
def add_nutrition_view(request):
    if request.method == 'POST':
        form = NutritionEntryForm(request.POST)
        if form.is_valid():
            nutrition = form.save(commit=False)
            nutrition.user = request.user
            nutrition.save()
            messages.success(request, 'Nutrition entry added!')
            return redirect('dashboard')
    else:
        form = NutritionEntryForm()
    return render(request, 'accounts/nutrition_form.html', {'form': form, 'title': 'Log Nutrition'})

@login_required
def add_exercise_view(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, 'Workout recorded!')
            return redirect('dashboard')
    else:
        form = ExerciseForm()
    return render(request, 'accounts/forms/add_exercise.html', {'form': form, 'title': 'Log Exercise'})

@login_required
def add_mood_view(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood tracked!')
            return redirect('dashboard')
    else:
        form = MoodEntryForm()
    return render(request, 'accounts/forms/add_mood.html', {'form': form, 'title': 'Track Mood'})

@login_required
def add_sleep_view(request):
    if request.method == 'POST':
        form = SleepEntryForm(request.POST)
        if form.is_valid():
            sleep = form.save(commit=False)
            sleep.user = request.user
            sleep.save()
            messages.success(request, 'Sleep log added!')
            return redirect('dashboard')
    else:
        form = SleepEntryForm()
    return render(request, 'accounts/forms/add_sleep.html', {'form': form, 'title': 'Log Sleep'})

@login_required
def add_medication_view(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            med = form.save(commit=False)
            med.user = request.user
            med.save()
            messages.success(request, 'Medication added!')
            return redirect('dashboard')
    else:
        form = MedicationForm()
    return render(request, 'accounts/forms/add_medication.html', {'form': form, 'title': 'Add Medication'})