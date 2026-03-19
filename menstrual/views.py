"""Menstrual cycle tracking views"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
import json

from .models import MenstrualProfile, DailyLog, CycleDay, CycleInsight
from .forms import MenstrualProfileForm, DailyLogForm
from .cycle_engine import (
    generate_cycle_data, get_daily_guidance, detect_cycle_patterns, 
    get_cycle_stats, PHASE_COLORS, PHASE_INFO
)


@login_required
@require_http_methods(["POST"])
def setup_profile(request):
    """Initialize or update menstrual profile"""
    try:
        data = json.loads(request.body)
        
        # Get or create profile
        profile, created = MenstrualProfile.objects.get_or_create(user=request.user)
        
        # Update fields
        if 'last_period_start' in data:
            profile.last_period_start = datetime.strptime(data['last_period_start'], '%Y-%m-%d').date()
        if 'avg_cycle_length' in data:
            profile.avg_cycle_length = int(data['avg_cycle_length'])
        if 'avg_period_length' in data:
            profile.avg_period_length = int(data['avg_period_length'])
        if 'pregnancy_goal' in data:
            profile.pregnancy_goal = data['pregnancy_goal']
        
        profile.save()
        
        # Generate cycle data for future dates
        generate_cycle_data(request.user, days_ahead=180)
        
        return JsonResponse({
            'success': True,
            'message': 'Profile setup complete',
            'profile': {
                'last_period_start': str(profile.last_period_start),
                'avg_cycle_length': profile.avg_cycle_length,
                'avg_period_length': profile.avg_period_length,
                'pregnancy_goal': profile.pregnancy_goal,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_profile(request):
    """Get current menstrual profile"""
    try:
        profile = MenstrualProfile.objects.get(user=request.user)
        return JsonResponse({
            'profile': {
                'last_period_start': str(profile.last_period_start),
                'avg_cycle_length': profile.avg_cycle_length,
                'avg_period_length': profile.avg_period_length,
                'pregnancy_goal': profile.pregnancy_goal,
                'next_period_estimate': str(profile.get_next_period_estimate()),
            }
        })
    except MenstrualProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def get_cycle_info(request):
    """Get today's cycle information"""
    try:
        profile = MenstrualProfile.objects.get(user=request.user)
        today = datetime.now().date()
        
        cycle_day = profile.get_current_cycle_day(today)
        phase = profile.get_cycle_phase(cycle_day)
        fertility = profile.get_fertility_level(cycle_day)
        
        # Get today's log if exists
        log = DailyLog.objects.filter(user=request.user, date=today).first()
        
        return JsonResponse({
            'today': str(today),
            'cycle_day': cycle_day,
            'cycle_length': profile.avg_cycle_length,
            'phase': phase,
            'phase_name': PHASE_INFO[phase]['name'],
            'phase_color': PHASE_COLORS[phase],
            'fertility_level': fertility,
            'next_period': str(profile.get_next_period_estimate()),
            'phase_info': PHASE_INFO[phase],
            'today_log': {
                'bleeding_level': log.bleeding_level if log else None,
                'pain_score': log.pain_score if log else None,
                'mood': log.mood if log else None,
                'symptoms': log.symptoms if log else [],
                'notes': log.notes if log else '',
            } if log else None,
        })
    except MenstrualProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found. Setup required.'}, status=404)


@login_required
@require_http_methods(["POST"])
def log_daily_data(request):
    """Log daily bleeding, pain, mood, and symptoms"""
    try:
        data = json.loads(request.body)
        date = datetime.strptime(data.get('date', datetime.now().isoformat()), '%Y-%m-%d').date()
        
        log, created = DailyLog.objects.update_or_create(
            user=request.user,
            date=date,
            defaults={
                'bleeding_level': data.get('bleeding_level', 'none'),
                'pain_score': int(data.get('pain_score', 0)),
                'mood': data.get('mood', ''),
                'symptoms': data.get('symptoms', []),
                'notes': data.get('notes', ''),
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': f"Daily log {'created' if created else 'updated'} for {date}",
            'log': {
                'date': str(log.date),
                'bleeding_level': log.bleeding_level,
                'pain_score': log.pain_score,
                'mood': log.mood,
                'symptoms': log.symptoms,
                'notes': log.notes,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_daily_logs(request):
    """Get daily logs for past N days (for graphs)"""
    try:
        days = int(request.GET.get('days', 90))
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        logs = DailyLog.objects.filter(
            user=request.user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')
        
        return JsonResponse({
            'logs': [{
                'date': str(log.date),
                'bleeding_level': log.bleeding_level,
                'pain_score': log.pain_score,
                'mood': log.mood,
                'symptoms': log.symptoms,
                'notes': log.notes,
            } for log in logs],
            'stats': get_cycle_stats(request.user, days=days),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_cycle_diagram_data(request):
    """Get cycle diagram data (28 segments with today highlighted)"""
    try:
        profile = MenstrualProfile.objects.get(user=request.user)
        today = datetime.now().date()
        current_cycle_day = profile.get_current_cycle_day(today)
        
        # Ensure we have a valid cycle length for the diagram (default to 28 if 0)
        cycle_length = profile.avg_cycle_length if profile.avg_cycle_length > 0 else 28
        
        # Get logs for current cycle
        cycle_start = today - timedelta(days=current_cycle_day - 1)
        cycle_end = cycle_start + timedelta(days=cycle_length - 1)
        
        logs = DailyLog.objects.filter(
            user=request.user,
            date__gte=cycle_start,
            date__lte=cycle_end
        )
        
        log_by_day = {(log.date - cycle_start).days + 1: log for log in logs}
        
        # Build 28 day segments
        segments = []
        for day in range(1, cycle_length + 1):
            phase = profile.get_cycle_phase(day)
            fertility = profile.get_fertility_level(day)
            log = log_by_day.get(day)
            
            segments.append({
                'day': day,
                'phase': phase,
                'phase_name': PHASE_INFO[phase]['name'],
                'phase_color': PHASE_COLORS[phase],
                'fertility': fertility,
                'is_today': day == current_cycle_day,
                'bleeding': log.bleeding_level if log else None,
                'pain': log.pain_score if log else None,
                'mood': log.mood if log else None,
            })
        
        return JsonResponse({
            'cycle_length': cycle_length,
            'current_day': current_cycle_day,
            'segments': segments,
        })
    except MenstrualProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)


@login_required
@require_http_methods(["GET"])
def get_guidance(request):
    """Get AI-generated daily guidance"""
    try:
        guidance = get_daily_guidance(request.user)
        
        if 'error' in guidance:
            return JsonResponse(guidance, status=400)
        
        return JsonResponse({
            'cycle_day': guidance['cycle_day'],
            'phase': guidance['phase'],
            'fertility': guidance['fertility'],
            'guidance': guidance['guidance'],
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["GET"])
def get_insights(request):
    """Get pattern insights and alerts"""
    try:
        patterns = detect_cycle_patterns(request.user)
        
        return JsonResponse({
            'insights': patterns,
            'stats': get_cycle_stats(request.user, days=90),
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def dashboard_view(request):
    """Dashboard page with menstrual tracking - form-based"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profile = MenstrualProfile.objects.get(user=request.user)
    except MenstrualProfile.DoesNotExist:
        return redirect('menstrual:setup')
    
    today = datetime.now().date()
    cycle_day = profile.get_current_cycle_day(today)
    phase = profile.get_cycle_phase(cycle_day)
    fertility = profile.get_fertility_level(cycle_day)
    
    # Get today's log
    today_log = DailyLog.objects.filter(user=request.user, date=today).first()
    
    # Handle form submission
    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=today_log)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            if not log.date:
                log.date = today
            log.save()
            messages.success(request, '✓ Daily log saved successfully!')
            return redirect('menstrual:dashboard')
    else:
        form = DailyLogForm(instance=today_log, initial={'date': today})
    
    # Get past logs for graphs
    end_date = today
    start_date = end_date - timedelta(days=90)
    logs = DailyLog.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('-date')
    
    # Get insights and stats
    insights = detect_cycle_patterns(request.user)
    stats = get_cycle_stats(request.user, days=90)
    
    return render(request, 'menstrual/cycle_dashboard.html', {
        'profile': profile,
        'today': today,
        'cycle_day': cycle_day,
        'phase': phase,
        'phase_name': PHASE_INFO[phase]['name'],
        'phase_color': PHASE_COLORS[phase],
        'fertility': fertility,
        'next_period': profile.get_next_period_estimate(),
        'form': form,
        'logs': logs,
        'insights': insights,
        'stats': stats,
    })


def setup_view(request):
    """Setup menstrual profile - form-based"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if profile already exists
    try:
        profile = MenstrualProfile.objects.get(user=request.user)
        return redirect('menstrual:dashboard')  # Already set up
    except MenstrualProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = MenstrualProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Generate cycle data for future dates
            generate_cycle_data(request.user, days_ahead=180)
            
            messages.success(request, '✓ Menstrual profile created successfully!')
            return redirect('menstrual:dashboard')
    else:
        form = MenstrualProfileForm()
    
    return render(request, 'menstrual/setup.html', {
        'form': form,
    })
