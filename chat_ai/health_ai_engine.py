"""
Health AI Engine - Personalized Health Recommendations
Uses Gemini AI to provide context-aware health advice based on user profile and health data
"""

import google.generativeai as genai
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.db.models import Avg, Sum
import json

from accounts.models import (
    HealthVital, NutritionEntry, Exercise, DailySteps, MoodEntry,
    SleepEntry, BloodSugarEntry, Profile, Medication
)

API_KEY = settings.GOOGLE_API_KEY
MODEL_ID = "gemini-2.5-flash"

# ==================== HEALTH DISCLAIMER ====================

HEALTH_DISCLAIMER = """
⚠️ **IMPORTANT HEALTH DISCLAIMER** ⚠️

This health app is a personal health management tool designed for tracking and basic health education ONLY.

❌ **This App is NOT:**
- A medical diagnosis tool
- A substitute for professional medical advice
- Licensed to treat or cure any disease
- A replacement for visiting a healthcare provider

✅ **What To Do:**
- Always consult a qualified healthcare professional before making medical decisions
- Seek immediate emergency care for urgent health issues (call your local emergency number)
- Use this app as a supplement to professional healthcare, not a replacement
- Report serious symptoms to a healthcare provider immediately

🔴 **EMERGENCY RED FLAGS - Seek immediate medical attention if you experience:**
- Chest pain or shortness of breath
- Severe headaches
- Loss of consciousness
- Difficulty speaking or vision changes
- Severe allergic reactions
- Uncontrollable bleeding
- Signs of stroke

**By using this app, you acknowledge that you understand these limitations and will seek professional medical advice as needed.**
"""

# ==================== HEALTH DATA ANALYZER ====================

class HealthAnalyzer:
    """Analyzes user health data to identify trends and risks"""
    
    @staticmethod
    def get_health_profile(user):
        """Extract comprehensive health profile"""
        profile = Profile.objects.filter(user=user).first()
        week_ago = timezone.now() - timedelta(days=7)
        
        # Get latest vitals
        latest_vital = HealthVital.objects.filter(user=user).latest('recorded_at') if HealthVital.objects.filter(user=user) else None
        
        # Calculate averages
        vitals = HealthVital.objects.filter(user=user, recorded_at__gte=week_ago)
        avg_bp = vitals.aggregate(Avg('blood_pressure_sys'))['blood_pressure_sys__avg']
        avg_hr = vitals.aggregate(Avg('heart_rate'))['heart_rate__avg']
        avg_weight = vitals.aggregate(Avg('weight'))['weight__avg']
        
        # Activity data
        exercises = Exercise.objects.filter(user=user, recorded_at__gte=week_ago)
        total_exercise_mins = exercises.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        
        steps = DailySteps.objects.filter(user=user, recorded_date__gte=week_ago.date())
        avg_steps = steps.aggregate(Avg('steps'))['steps__avg'] or 0
        
        # Mental health
        moods = MoodEntry.objects.filter(user=user, recorded_at__gte=week_ago)
        mood_values = {'EXCELLENT': 5, 'GOOD': 4, 'NEUTRAL': 3, 'POOR': 2, 'VERY_POOR': 1}
        mood_scores = [mood_values.get(m.mood, 0) for m in moods]
        avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else 3
        
        # Sleep
        sleeps = SleepEntry.objects.filter(user=user, recorded_date__gte=week_ago.date())
        avg_sleep = sleeps.aggregate(Avg('sleep_duration_hours'))['sleep_duration_hours__avg'] or 0
        
        # Medications
        active_meds = Medication.objects.filter(user=user, is_active=True)
        
        return {
            'age': profile.date_of_birth.year if profile and profile.date_of_birth else None,
            'health_focus': profile.health_focus if profile else 'GENERAL',
            'latest_vital': {
                'weight': latest_vital.weight if latest_vital else None,
                'height': latest_vital.height if latest_vital else None,
                'blood_pressure': f"{latest_vital.blood_pressure_sys}/{latest_vital.blood_pressure_dia}" if latest_vital else None,
                'heart_rate': latest_vital.heart_rate if latest_vital else None,
                'bmi': latest_vital.bmi if latest_vital else None,
            },
            'weekly_averages': {
                'blood_pressure_systolic': round(avg_bp, 1) if avg_bp else None,
                'heart_rate': round(avg_hr, 1) if avg_hr else None,
                'weight': round(avg_weight, 1) if avg_weight else None,
            },
            'activity': {
                'exercise_minutes': total_exercise_mins,
                'average_daily_steps': round(avg_steps, 0),
            },
            'mental_health': {
                'average_mood_score': round(avg_mood, 1),
                'mood_status': 'good' if avg_mood >= 3.5 else 'requires_attention',
                'average_sleep_hours': round(avg_sleep, 1),
            },
            'medications_count': active_meds.count(),
        }
    
    @staticmethod
    def identify_health_risks(health_profile):
        """Identify potential health risks"""
        risks = []
        
        # Blood pressure risks
        bp_systolic = health_profile.get('weekly_averages', {}).get('blood_pressure_systolic')
        if bp_systolic:
            if bp_systolic >= 140:
                risks.append({'risk': 'HIGH_BLOOD_PRESSURE', 'severity': 'high'})
            elif bp_systolic >= 130:
                risks.append({'risk': 'ELEVATED_BLOOD_PRESSURE', 'severity': 'medium'})
        
        # Activity risks
        activity = health_profile.get('activity', {})
        if activity.get('exercise_minutes', 0) < 60:
            risks.append({'risk': 'LOW_PHYSICAL_ACTIVITY', 'severity': 'medium'})
        if activity.get('average_daily_steps', 0) < 5000:
            risks.append({'risk': 'SEDENTARY_LIFESTYLE', 'severity': 'medium'})
        
        # Mental health risks
        mental = health_profile.get('mental_health', {})
        if mental.get('average_mood_score', 3) < 2.5:
            risks.append({'risk': 'LOW_MOOD', 'severity': 'high'})
        
        # Sleep risks
        if mental.get('average_sleep_hours', 7) < 6:
            risks.append({'risk': 'INSUFFICIENT_SLEEP', 'severity': 'high'})
        if mental.get('average_sleep_hours', 7) > 9:
            risks.append({'risk': 'EXCESSIVE_SLEEP', 'severity': 'medium'})
        
        # BMI risks
        bmi = health_profile.get('latest_vital', {}).get('bmi')
        if bmi:
            if bmi > 30:
                risks.append({'risk': 'OVERWEIGHT', 'severity': 'medium'})
            elif bmi < 18.5:
                risks.append({'risk': 'UNDERWEIGHT', 'severity': 'medium'})
        
        return risks
    
    @staticmethod
    def get_age_category(age):
        """Categorize age for recommendations"""
        if age is None:
            return 'UNKNOWN'
        if age < 13:
            return 'CHILD'
        elif age < 20:
            return 'TEENAGER'
        elif age < 46:
            return 'ADULT'
        else:
            return 'OLDER_ADULT'


# ==================== PERSONALIZED RECOMMENDATIONS ====================

class HealthRecommendationEngine:
    """Generates AI-powered personalized health recommendations"""
    
    @staticmethod
    def get_ai_personalized_tips(user, context):
        """Get AI-generated personalized health tips"""
        try:
            # Build context prompt
            prompt = f"""You are a health education AI assistant. Based on this user's health profile, provide 3 specific, actionable health tips.

User Health Profile:
- Age: {context.get('age', 'Unknown')} years
- Health Focus: {context.get('health_focus', 'General')}
- BMI: {context.get('latest_vital', {}).get('bmi', 'Not recorded')}
- Weekly Exercise: {context.get('activity', {}).get('exercise_minutes', 0)} minutes
- Average Sleep: {context.get('mental_health', {}).get('average_sleep_hours', 0)} hours
- Mood Status: {context.get('mental_health', {}).get('mood_status', 'Unknown')}
- Blood Pressure (Systolic): {context.get('weekly_averages', {}).get('blood_pressure_systolic', 'Not recorded')} mmHg

Risks Identified: {json.dumps(context.get('risks', []))}

Please provide:
1. THREE specific health tips (numbered 1, 2, 3)
2. Each tip should be actionable and specific to their profile
3. Keep each tip to 1-2 sentences
4. Focus on prevention and wellness

Format your response as:
Tip 1: [Your tip here]
Tip 2: [Your tip here]
Tip 3: [Your tip here]

Make it practical for someone in Tanzania context (consider local food, climate, accessibility)."""

            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Unable to generate AI tips at this moment. Error: {str(e)}"
    
    @staticmethod
    def get_nutrition_advice(user):
        """Get AI nutrition advice based on health profile"""
        try:
            # Get recent nutrition data
            week_ago = timezone.now() - timedelta(days=7)
            nutrition = NutritionEntry.objects.filter(user=user, recorded_at__gte=week_ago)
            total_calories = nutrition.aggregate(Sum('calories'))['calories__sum'] or 0
            entry_count = nutrition.count()
            avg_calories = total_calories / 7  # per day average
            
            prompt = f"""As a nutrition educator, provide 2-3 practical nutrition tips for someone in Tanzania.

Context:
- Average daily calories recorded: {avg_calories:.0f} calories
- Meals tracked in past week: {entry_count}
- Health goals: Weight management and disease prevention

Please provide:
1. Specific local food recommendations (consider Tanzanian staples like ugali, beans, coconut, etc.)
2. Practical meal planning tips for daily life
3. Water intake importance

Keep it brief and actionable."""

            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return "Unable to generate nutrition advice at this moment."
    
    @staticmethod
    def get_mental_wellness_tips(user):
        """Get AI mental wellness recommendations"""
        try:
            # Get mood data
            week_ago = timezone.now() - timedelta(days=7)
            moods = MoodEntry.objects.filter(user=user, recorded_at__gte=week_ago)
            mood_values = {'EXCELLENT': 5, 'GOOD': 4, 'NEUTRAL': 3, 'POOR': 2, 'VERY_POOR': 1}
            mood_scores = [mood_values.get(m.mood, 0) for m in moods]
            avg_mood = sum(mood_scores) / len(mood_scores) if mood_scores else 3
            
            sleep = SleepEntry.objects.filter(user=user, recorded_date__gte=week_ago.date())
            avg_sleep = sleep.aggregate(Avg('sleep_duration_hours'))['sleep_duration_hours__avg'] or 7
            
            prompt = f"""As a mental wellness expert, provide practical mental health tips.

Context:
- Average mood score (1-5): {avg_mood:.1f}
- Average sleep hours: {avg_sleep:.1f}
- Region: Tanzania

Provide 3 practical tips for:
1. Stress management
2. Improving sleep quality
3. Maintaining positive mental health

Consider local context and cultural practices. Keep it concise."""

            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_ID)
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return "Unable to generate wellness tips at this moment."


# ==================== HELPER FUNCTIONS ====================

def get_health_summary(user):
    """Get comprehensive health summary for user"""
    analyzer = HealthAnalyzer()
    health_profile = analyzer.get_health_profile(user)
    risks = analyzer.identify_health_risks(health_profile)
    
    return {
        'profile': health_profile,
        'risks': risks,
        'disclaimer': HEALTH_DISCLAIMER
    }


def get_personalized_ai_recommendations(user):
    """Get all personalized AI recommendations for user"""
    summary = get_health_summary(user)
    engine = HealthRecommendationEngine()
    
    return {
        'health_summary': summary['profile'],
        'identified_risks': summary['risks'],
        'personalized_tips': engine.get_ai_personalized_tips(user, summary['profile']),
        'nutrition_advice': engine.get_nutrition_advice(user),
        'wellness_tips': engine.get_mental_wellness_tips(user),
        'disclaimer': HEALTH_DISCLAIMER
    }
