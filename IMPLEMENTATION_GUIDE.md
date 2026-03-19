"""
IMPLEMENTATION GUIDE - HEALTH APP MVP
=====================================

This guide provides step-by-step instructions to set up and run the health management application.

## PHASE 1: SETUP & CONFIGURATION

### 1.1 Install Dependencies
```bash
pip install django djangorestframework django-cors-headers google-genai
```

### 1.2 Create Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 1.3 Create Superuser (Admin)
```bash
python manage.py createsuperuser
# Phone number: +255700000000
# Password: your_password
```

### 1.4 Run Development Server
```bash
python manage.py runserver
```

Access at: http://localhost:8000

## PHASE 2: CORE FEATURES

### 2.1 Health Vitals Tracking
✅ Models: HealthVital, MedicalHistory
✅ Endpoints: /api/vitals/*
✅ Dashboard: Quick vital signs display

**To Log Vitals:**
```python
POST /api/vitals/
{
    "weight": 70.5,
    "height": 175,
    "blood_pressure_sys": 120,
    "blood_pressure_dia": 80,
    "heart_rate": 72
}
```

### 2.2 Nutrition Tracking
✅ Models: NutritionEntry, DailyNutritionGoal, WaterIntake
✅ Endpoints: /api/nutrition/*, /api/water/*
✅ Dashboard: Daily calorie tracking, nutrition goals

**To Log Meal:**
```python
POST /api/nutrition/
{
    "meal_type": "BREAKFAST",
    "food_items": "[{"name": "rice", "quantity": "2 cups"}]",
    "calories": 350,
    "protein_g": 8,
    "carbs_g": 60,
    "fat_g": 5
}
```

### 2.3 Physical Activity Tracking
✅ Models: Exercise, DailySteps, FitnessGoal
✅ Endpoints: /api/exercises/*, /api/steps/*
✅ Dashboard: Weekly exercise summary, step counter

### 2.4 Mental Health & Wellness
✅ Models: MoodEntry, SleepEntry, MindfulnessSession
✅ Endpoints: /api/mood/*, /api/sleep/*, /api/mindfulness/*
✅ Dashboard: Mood trends, sleep quality, wellness activities

### 2.5 Medication Management
✅ Models: Medication, MedicationReminder, MedicationAdherence, MedicalAppointment
✅ Endpoints: /api/medications/*, /api/appointments/*
✅ Features: Track medications, set reminders, monitor adherence, schedule appointments

## PHASE 3: AI-POWERED FEATURES

### 3.1 Health Insights Engine
✅ Module: health_ai_engine.py
✅ Features: 
   - Health profile analysis
   - Risk identification
   - Personalized recommendations
   - Age-based advice

**Usage:**
```python
from chat_ai.health_ai_engine import get_personalized_ai_recommendations

recommendations = get_personalized_ai_recommendations(user)
# Returns: health_summary, risks, AI tips, nutrition advice, wellness tips
```

### 3.2 AI Personalization
✅ Endpoints: /chat-ai/api/health-summary/
✅ Features:
   - Personalized health tips
   - Nutrition advice (local Tanzanian foods)
   - Exercise recommendations
   - Mental wellness tips
   - Health Q&A with AI

### 3.3 Smart Health Chat
✅ Endpoint: /chat-ai/api/send/
✅ Features:
   - Context-aware responses
   - Health education
   - Symptom guidance (non-diagnostic)
   - Medication information

## PHASE 4: ANALYTICS & REPORTING

### 4.1 Weekly Health Reports
✅ Model: HealthReport
✅ Endpoint: /health-reports/generate/
✅ Features:
   - Average vitals
   - Activity summary
   - Nutrition analysis
   - Mental health trends
   - Risk identification
   - AI recommendations

### 4.2 Health Risk Detection
✅ Automatic detection for:
   - High blood pressure
   - Low physical activity
   - Insufficient sleep
   - Low mood/mental health concerns
   - Overweight/underweight
   - High blood sugar

## PHASE 5: COMPLIANCE & SAFETY

### 5.1 Health Disclaimers
✅ Display on all health advice
✅ Clearly states app is NOT medical diagnosis
✅ Encourages consulting healthcare professionals
✅ Emergency red-flag detection

### 5.2 Data Privacy
- HTTPS recommended for production
- User data encryption recommended
- Secure password hashing (Django default)
- CSRF protection enabled

### 5.3 Emergency Escalation
✅ Red flag alerts for:
   - Chest pain
   - Severe symptoms
   - Emergency conditions
✅ Guidance to seek immediate medical attention

## TESTING THE APPLICATION

### Test 1: Create User & Profile
```python
# Create test user
POST /api/users/
{
    "u_phone_number": "+255700000001",
    "password": "test123"
}

# Create profile
POST /api/users/{id}/profile/
{
    "date_of_birth": "1990-01-01",
    "health_focus": "GENERAL"
}
```

### Test 2: Log Health Data
```python
# Log vital signs
POST /api/vitals/
{
    "weight": 70,
    "height": 175,
    "blood_pressure_sys": 120,
    "blood_pressure_dia": 80,
    "heart_rate": 72
}

# Log meal
POST /api/nutrition/
{
    "meal_type": "BREAKFAST",
    "food_items": "[{"name": "eggs", "quantity": "2"}]",
    "calories": 200
}

# Log exercise
POST /api/exercises/
{
    "exercise_type": "Running",
    "intensity": "MODERATE",
    "duration_minutes": 30,
    "calories_burned": 250
}

# Log mood
POST /api/mood/
{
    "mood": "GOOD",
    "stress_level": 3,
    "anxiety_level": 2
}

# Log sleep
POST /sleep/
{
    "sleep_duration_hours": 7.5,
    "sleep_quality": 8,
    "bed_time": "22:30",
    "wake_time": "06:00"
}
```

### Test 3: Get AI Recommendations
```
GET /chat-ai/api/health-summary/
Returns: Personalized health summary with AI insights

GET /chat-ai/api/nutrition-advice/
Returns: AI nutrition recommendations

GET /chat-ai/api/wellness-tips/
Returns: Mental wellness recommendations

GET /chat-ai/api/exercise-recommendations/
Returns: Customized exercise plan
```

### Test 4: Generate Health Report
```
POST /health-reports/generate/
Returns: Weekly health analysis with risks and recommendations
```

## DASHBOARD FEATURES

### Home Dashboard (/)
- User welcome message
- Latest vital signs
- Today's mood and sleep
- Quick action buttons
- AI insights preview

### Health Tracking
- Log vital signs
- Nutrition logging with meal tracking
- Exercise and step tracking
- Blood sugar monitoring
- Water intake tracking

### Mental Wellness
- Daily mood check-ins
- Sleep tracking
- Mindfulness activities
- Stress management
- Mental health trends

### Medication Management
- Add/edit medications
- Set medication reminders
- Track medication adherence
- Schedule doctor appointments

### AI Features
- Personalized health tips (AI-generated)
- Nutrition advice specific to Tanzanian context
- Exercise recommendations based on profile
- Mental wellness guidance
- Health education chat

### Reports
- Weekly health summary
- Progress visualization
- Risk identification
- Personalized recommendations

## FUTURE ENHANCEMENTS (Optional)

1. **Wearable Integration**
   - Smartwatch sync
   - Real-time vital tracking
   - Activity data import

2. **Telemedicine**
   - Doctor video consultations
   - Prescription management
   - Medical records storage

3. **Community Features**
   - Health challenges
   - Progress sharing
   - Support groups

4. **Advanced Analytics**
   - Predictive health alerts
   - Long-term trend analysis
   - Risk forecasting

5. **Local Integration**
   - Emergency services database
   - Nearby clinic locator
   - Local health information

## TROUBLESHOOTING

### Migration Issues
```bash
# If migrations fail, reset database (development only!)
python manage.py flush
python manage.py makemigrations
python manage.py migrate
```

### API Errors
- Check authentication headers
- Verify request format (JSON)
- Check for required fields
- Review error response message

### AI API Issues
- Verify Google GenAI API key
- Check internet connection
- Review API rate limits
- Check API documentation

## PRODUCTION CHECKLIST

Before deploying to production:

- [ ] Set DEBUG = False in settings.py
- [ ] Configure allowed hosts
- [ ] Use HTTPS
- [ ] Implement database backups
- [ ] Set up error logging
- [ ] Configure email for notifications
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Set up monitoring
- [ ] Configure health disclaimers
- [ ] Test all endpoints
- [ ] Review security settings
- [ ] Set up CORS properly
- [ ] Configure static files

## SUPPORT & DOCUMENTATION

- API Documentation: See API_DOCUMENTATION.md
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Google GenAI: https://ai.google.dev/

---
Created: January 30, 2026
Version: 1.0 (MVP)
