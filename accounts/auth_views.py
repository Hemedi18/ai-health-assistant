"""
Professional Authentication Views for Afya Yako AI
===================================================
Handles login, registration, logout, and user authentication
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg, Sum
from datetime import timedelta
from .models import User, Profile, HealthVital, MoodEntry, SleepEntry
from .forms import UserRegistrationForm, UserLoginForm
import json


@require_http_methods(["GET", "POST"])
@csrf_protect
def home_view(request):
    """Landing page - shows before authentication"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'app_name': 'Afya Yako AI',
        'tagline': 'Your Personal AI Health Assistant',
        'features': [
            {
                'icon': '📊',
                'title': 'Health Tracking',
                'description': 'Track vitals, nutrition, exercise, and mood daily'
            },
            {
                'icon': '🤖',
                'title': 'AI Personalization',
                'description': 'Get personalized health recommendations based on your data'
            },
            {
                'icon': '💊',
                'title': 'Medication Manager',
                'description': 'Manage medications and appointment reminders'
            },
            {
                'icon': '📱',
                'title': 'Mental Wellness',
                'description': 'Track mood, sleep, and mindfulness sessions'
            },
            {
                'icon': '📈',
                'title': 'Health Reports',
                'description': 'Get weekly insights and health analysis'
            },
            {
                'icon': '🚨',
                'title': 'Safety First',
                'description': 'Emergency alerts and health safety protocols'
            },
        ]
    }
    return render(request, 'accounts/home.html', context)


@require_http_methods(["GET", "POST"])
@csrf_protect
def login_view(request):
    """Professional login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            u_phone_number = form.cleaned_data['u_phone_number']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=u_phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome back!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid phone number or password.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'app_name': 'Afya Yako AI',
    }
    return render(request, 'accounts/login.html', context)


@require_http_methods(["GET", "POST"])
@csrf_protect
def register_view(request):
    """Professional registration page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create new user
            u_phone_number = form.cleaned_data['u_phone_number']
            password = form.cleaned_data['password']
            health_focus = form.cleaned_data.get('health_focus', 'GENERAL')
            
            user = User.objects.create_user(u_phone_number, password)
            
            # Create user profile with health focus
            Profile.objects.create(
                user=user,
                health_focus=health_focus,
            )
            
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'app_name': 'Afya Yako AI',
    }
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
def dashboard_view(request):
    """Main dashboard after login - shows important health info"""
    user = request.user
    
    # Get latest health data
    latest_vital = user.vitals.latest('recorded_at') if user.vitals.exists() else None
    today_mood = user.mood_entries.filter(date=timezone.now().date()).first()
    today_sleep = user.sleep_entries.filter(date=timezone.now().date()).first()
    today_steps = user.daily_steps.filter(date=timezone.now().date()).first()
    today_water = user.water_intake.filter(recorded_at__date=timezone.now().date()).aggregate(Sum('amount_ml'))['amount_ml__sum'] or 0
    
    # Get pending medications
    pending_meds = user.medications.filter().count()  # Medications don't have is_completed
    upcoming_appointments = user.appointments.filter(
        appointment_date__gte=timezone.now()
    ).order_by('appointment_date')[:3]
    
    # Get health report
    latest_report = user.health_reports.latest('generated_at') if user.health_reports.exists() else None
    
    context = {
        'user': user,
        'latest_vital': latest_vital,
        'today_mood': today_mood,
        'today_sleep': today_sleep,
        'today_steps': today_steps,
        'today_water': today_water,
        'pending_meds': pending_meds,
        'upcoming_appointments': upcoming_appointments,
        'latest_report': latest_report,
        'page_title': 'Health Dashboard',
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def profile_view(request):
    """User profile page"""
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    
    # Get health statistics
    vitals_count = HealthVital.objects.filter(user=user).count()
    mood_count = MoodEntry.objects.filter(user=user).count()
    sleep_count = SleepEntry.objects.filter(user=user).count()
    
    context = {
        'user': user,
        'profile': profile,
        'vitals_count': vitals_count,
        'mood_count': mood_count,
        'sleep_count': sleep_count,
        'page_title': 'My Profile',
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def health_summary_view(request):
    """Comprehensive health summary page"""
    from django.db.models import Avg, Count, Sum
    
    user = request.user
    today = timezone.now().date()
    this_week = timezone.now() - timedelta(days=7)
    
    # Vitals summary
    weekly_vitals = user.vitals.filter(
        recorded_at__gte=this_week
    ).values('recorded_at__date').annotate(
        avg_systolic=Avg('blood_pressure_sys'),
        avg_diastolic=Avg('blood_pressure_dia'),
        avg_heart_rate=Avg('heart_rate'),
    )
    
    # Nutrition summary
    daily_nutrition = user.nutrition_entries.filter(
        recorded_at__date=today
    ).aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein_g'),
        total_carbs=Sum('carbs_g'),
        total_fat=Sum('fat_g'),
    )
    
    # Exercise summary
    today_exercise = user.exercises.filter(
        recorded_at__date=today
    ).aggregate(
        total_duration=Sum('duration_minutes'),
        total_calories_burned=Sum('calories_burned'),
    )
    
    # Mental health summary
    mood_data = user.mood_entries.filter(
        recorded_at__date__gte=this_week
    ).values('recorded_at__date').annotate(
        avg_stress=Avg('stress_level'),
        avg_anxiety=Avg('anxiety_level'),
    )
    
    context = {
        'user': user,
        'page_title': 'Health Summary',
        'weekly_vitals': list(weekly_vitals),
        'daily_nutrition': daily_nutrition,
        'today_exercise': today_exercise,
        'mood_data': list(mood_data),
    }
    return render(request, 'accounts/health_summary.html', context)
