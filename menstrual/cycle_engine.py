"""Menstrual cycle logic and AI guidance generation"""
from datetime import datetime, timedelta
from .models import MenstrualProfile, DailyLog, CycleDay, CycleInsight
import google.generativeai as genai

# Phase info
PHASE_COLORS = {
    'menstrual': '#FF4444',
    'follicular': '#FFB6D9',
    'ovulation': '#44FF44',
    'luteal': '#9966CC',
}

PHASE_INFO = {
    'menstrual': {
        'name': 'Menstrual',
        'energy': 'Low to moderate',
        'mood': 'May experience mood changes',
        'appetite': 'Variable',
        'libido': 'May vary',
    },
    'follicular': {
        'name': 'Follicular',
        'energy': 'Increasing',
        'mood': 'Improved',
        'appetite': 'Stable to decreased',
        'libido': 'Gradually increasing',
    },
    'ovulation': {
        'name': 'Ovulation',
        'energy': 'Peak',
        'mood': 'Energetic and confident',
        'appetite': 'May increase',
        'libido': 'Peak',
    },
    'luteal': {
        'name': 'Luteal',
        'energy': 'Declining',
        'mood': 'May experience PMS-related changes',
        'appetite': 'May increase',
        'libido': 'Declining',
    },
}


def generate_cycle_data(user, days_ahead=90):
    """Generate CycleDay records for the next N days"""
    try:
        profile = user.menstrual_profile
    except:
        return False

    today = datetime.now().date()
    for i in range(days_ahead):
        date = today + timedelta(days=i)
        cycle_day = profile.get_current_cycle_day(date)
        phase = profile.get_cycle_phase(cycle_day)
        fertility = profile.get_fertility_level(cycle_day)

        CycleDay.objects.update_or_create(
            user=user,
            date=date,
            defaults={
                'cycle_day_number': cycle_day,
                'phase': phase,
                'fertility_level': fertility,
            }
        )
    return True


def get_daily_guidance(user, date=None):
    """Generate AI-powered daily guidance based on cycle day"""
    if date is None:
        date = datetime.now().date()

    try:
        profile = user.menstrual_profile
        cycle_day = profile.get_current_cycle_day(date)
        phase = profile.get_cycle_phase(cycle_day)
        fertility = profile.get_fertility_level(cycle_day)

        # Get today's log if exists
        log = DailyLog.objects.filter(user=user, date=date).first()

        # Build prompt for AI
        prompt = f"""Generate brief, supportive daily health guidance for a woman in the {phase} phase of her menstrual cycle (day {cycle_day} of {profile.avg_cycle_length}).

Pregnancy goal: {profile.get_pregnancy_goal_display() if hasattr(profile, 'get_pregnancy_goal_display') else profile.pregnancy_goal}

Cycle phase characteristics:
- Energy: {PHASE_INFO[phase]['energy']}
- Mood: {PHASE_INFO[phase]['mood']}
- Appetite: {PHASE_INFO[phase]['appetite']}
- Libido: {PHASE_INFO[phase]['libido']}
- Fertility level: {fertility}

{f"Today's logged symptoms: Bleeding ({log.bleeding_level}), Pain ({log.pain_score}/5), Mood ({log.mood})" if log else ""}

Provide:
1. How she might feel today (normal and expected)
2. Recommended exercise type
3. Nutrition tips
4. Self-care suggestion
5. If fertility is high or medium, relevant contraception/conception guidance based on her goal

Keep it positive, practical, and non-medical. Under 150 words."""

        genai.configure(api_key="AIzaSyD38OvL0zSuVLMMc1mrhq54Dko0F0gdO50")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {
            'cycle_day': cycle_day,
            'phase': phase,
            'fertility': fertility,
            'guidance': response.text,
        }
    except Exception as e:
        return {
            'error': str(e),
            'cycle_day': cycle_day if 'cycle_day' in locals() else None,
        }


def detect_cycle_patterns(user):
    """Analyze logs to detect trends and patterns"""
    logs = DailyLog.objects.filter(user=user).order_by('-date')[:60]  # Last ~2 cycles
    if len(logs) < 10:
        return []

    insights = []

    # Check for heavy bleeding patterns
    heavy_days = [l for l in logs if l.bleeding_level in ['heavy', 'medium']]
    if len(heavy_days) > 10:
        insights.append({
            'type': 'pattern',
            'title': 'Extended or heavy bleeding detected',
            'description': 'Your logs show consistent heavy or medium bleeding. Consider tracking with a healthcare provider.',
        })

    # Check for pain
    high_pain_logs = [l for l in logs if l.pain_score >= 4]
    if len(high_pain_logs) > 0:
        insights.append({
            'type': 'alert',
            'title': 'Significant menstrual pain noted',
            'description': 'You\'ve logged pain levels of 4+. OTC pain relief or a warm compress may help. Consult a provider if severe.',
        })

    # Check for mood patterns
    sad_moods = [l for l in logs if l.mood == 'sad']
    if len(sad_moods) >= 5:
        insights.append({
            'type': 'pattern',
            'title': 'Mood changes during cycle',
            'description': 'You may experience mood changes during the luteal phase. Stress management and self-care can help.',
        })

    return insights


def get_cycle_stats(user, days=90):
    """Get summary statistics for the past N days"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    logs = DailyLog.objects.filter(user=user, date__gte=start_date, date__lte=end_date).order_by('-date')

    if not logs:
        return {}

    bleeding_days = logs.filter(bleeding_level__in=['light', 'medium', 'heavy']).count()
    avg_pain = sum([l.pain_score for l in logs]) / len(logs) if logs else 0

    moods = [l.mood for l in logs if l.mood]
    most_common_mood = max(set(moods), key=moods.count) if moods else None

    return {
        'total_logs': len(logs),
        'bleeding_days': bleeding_days,
        'avg_pain_score': round(avg_pain, 1),
        'most_common_mood': most_common_mood,
        'date_range': f"{start_date} to {end_date}",
    }
