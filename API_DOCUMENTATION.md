"""
HEALTH APP API DOCUMENTATION
=============================

This document provides a complete overview of the health management API endpoints.

## Authentication
Most endpoints require user authentication. Include user ID or authentication token in requests.

## BASE URL
http://localhost:8000/api/

## HEALTH VITALS ENDPOINTS

### Get Latest Vital Signs
GET /vitals/latest/
- Returns: Latest vital signs for the user
- Response: {
    "id": 1,
    "weight": 70.5,
    "height": 175,
    "blood_pressure_sys": 120,
    "blood_pressure_dia": 80,
    "heart_rate": 72,
    "bmi": 23.02,
    "recorded_at": "2026-01-30T10:30:00Z"
  }

### Get Weekly Vital Averages
GET /vitals/weekly_average/
- Returns: Weekly averages of vital signs

### Create Vital Record
POST /vitals/
- Body: {
    "weight": 70.5,
    "height": 175,
    "blood_pressure_sys": 120,
    "blood_pressure_dia": 80,
    "heart_rate": 72
  }

## NUTRITION ENDPOINTS

### Log Meal
POST /nutrition/
- Body: {
    "meal_type": "BREAKFAST",
    "food_items": "[{"name": "rice", "quantity": "2 cups"}]",
    "calories": 350,
    "protein_g": 8,
    "carbs_g": 60,
    "fat_g": 5,
    "notes": "With beans"
  }

### Get Today's Nutrition Summary
GET /nutrition/today_summary/
- Returns: Today's total calories, macros, remaining calories

### Get Nutrition Goals
GET /nutrition-goals/
- Returns: Daily nutrition targets

### Update Nutrition Goals
POST /nutrition-goals/
- Body: {
    "target_calories": 2000,
    "target_protein_g": 50,
    "special_diet": "diabetic"
  }

### Log Water Intake
POST /water/
- Body: {
    "amount_ml": 250
  }

### Get Today's Water Intake
GET /water/today_total/

## FITNESS & ACTIVITY ENDPOINTS

### Log Exercise
POST /exercises/
- Body: {
    "exercise_type": "Running",
    "intensity": "MODERATE",
    "duration_minutes": 30,
    "calories_burned": 250,
    "notes": "Morning run"
  }

### Get Weekly Exercise Summary
GET /exercises/weekly_summary/

### Log Daily Steps
POST /steps/
- Body: {
    "steps": 8000,
    "distance_km": 6.4
  }

### Get Fitness Goals
GET /fitness-goals/

### Update Fitness Goals
POST /fitness-goals/
- Body: {
    "target_steps_daily": 10000,
    "target_exercise_minutes_weekly": 150
  }

## MENTAL HEALTH ENDPOINTS

### Log Mood
POST /mood/
- Body: {
    "mood": "GOOD",
    "triggers": "work",
    "anxiety_level": 3,
    "stress_level": 4,
    "notes": "Productive day"
  }

### Get Weekly Mood Trends
GET /mood/weekly_trends/

### Log Sleep
POST /sleep/
- Body: {
    "sleep_duration_hours": 7.5,
    "sleep_quality": 8,
    "bed_time": "22:30",
    "wake_time": "06:00",
    "notes": "Good sleep"
  }

### Get Weekly Sleep Average
GET /sleep/weekly_average/

### Log Mindfulness Session
POST /mindfulness/
- Body: {
    "session_type": "MEDITATION",
    "duration_minutes": 15,
    "feeling_before": "stressed",
    "feeling_after": "calm"
  }

### Get Monthly Mindfulness Stats
GET /mindfulness/monthly_stats/

## MEDICATION ENDPOINTS

### Add Medication
POST /medications/
- Body: {
    "medication_name": "Aspirin",
    "dosage": "100mg",
    "frequency": "ONCE_DAILY",
    "reason": "Pain relief",
    "start_date": "2026-01-01",
    "side_effects": "None",
    "is_active": true
  }

### Get Active Medications
GET /medications/active/

### Log Medication Adherence
POST /medication-adherence/
- Body: {
    "medication": 1,
    "scheduled_date": "2026-01-30",
    "was_taken": true,
    "time_taken": "08:00"
  }

### Get Adherence Rate
GET /medication-adherence/adherence_rate/

### Schedule Medical Appointment
POST /appointments/
- Body: {
    "doctor_name": "Dr. Smith",
    "clinic_name": "City Hospital",
    "appointment_date": "2026-02-15T10:00:00Z",
    "reason": "Checkup",
    "notes": "Annual checkup"
  }

### Get Upcoming Appointments
GET /appointments/upcoming/

## BLOOD SUGAR ENDPOINTS

### Log Blood Sugar
POST /blood-sugar/
- Body: {
    "blood_sugar_mg_dl": 120,
    "measurement_time": "FASTING",
    "notes": "Morning reading"
  }

### Get Weekly Blood Sugar Average
GET /blood-sugar/weekly_average/

## HEALTH REPORTS

### Generate Weekly Report
POST /health-reports/generate/
- Returns: Comprehensive weekly health analysis with risks and recommendations

### Get Health Reports
GET /health-reports/

## AI FEATURES

### Get Health Summary with AI Recommendations
GET /chat-ai/api/health-summary/
- Returns: Personalized health profile and AI recommendations

### Get Nutrition Advice
GET /chat-ai/api/nutrition-advice/
- Returns: AI-generated nutrition tips for Tanzanian context

### Get Wellness Tips
GET /chat-ai/api/wellness-tips/
- Returns: Mental health and wellness recommendations

### Get Exercise Recommendations
GET /chat-ai/api/exercise-recommendations/
- Returns: Personalized exercise plan based on profile

### Ask Health Question
POST /chat-ai/api/ask-question/
- Body: {
    "question": "Is it normal to have high blood pressure at my age?"
  }
- Returns: Educational response (not medical diagnosis)

### Health Chat
POST /chat-ai/api/send/
- Body: {
    "message": "Tell me about healthy diet"
  }
- Returns: AI response with health context

## ERROR RESPONSES

400 Bad Request - Invalid data provided
401 Unauthorized - Authentication required
404 Not Found - Resource not found
500 Server Error - Internal server error

## USAGE EXAMPLE

```python
import requests

# Get user's latest vitals
response = requests.get(
    'http://localhost:8000/api/vitals/latest/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'}
)
print(response.json())

# Log a meal
response = requests.post(
    'http://localhost:8000/api/nutrition/',
    headers={'Authorization': 'Bearer YOUR_TOKEN'},
    json={
        'meal_type': 'BREAKFAST',
        'food_items': '[{"name": "ugali", "quantity": "2 cups"}]',
        'calories': 350
    }
)
print(response.json())
```

## IMPORTANT HEALTH DISCLAIMERS

⚠️ **This app is NOT:**
- A medical diagnosis tool
- A substitute for professional medical advice
- Licensed to treat or cure diseases
- A replacement for healthcare providers

✅ **Always:**
- Consult qualified healthcare professionals
- Seek emergency care for urgent issues
- Use this app as a supplement, not replacement
- Report serious symptoms to healthcare providers

🔴 **Emergency Red Flags:**
- Chest pain or shortness of breath
- Severe headaches
- Loss of consciousness
- Difficulty speaking
- Severe allergic reactions
- Uncontrollable bleeding

## LOCAL CONTEXT (TANZANIA)

The AI features are optimized for the Tanzanian context:
- Food recommendations use local staples (ugali, beans, cassava, coconut, etc.)
- Exercise plans consider local climate and accessibility
- Health information respects cultural practices
- Resources address common health concerns in East Africa

## GETTING STARTED

1. Create a user account with phone number
2. Complete your health profile (age, gender, health focus)
3. Start logging health data through the API or dashboard
4. Access AI recommendations based on your profile
5. Generate weekly health reports
6. Use AI chat for health education questions

## SUPPORT

For issues or questions, contact support@healthapp.tz

---
Last Updated: January 30, 2026
Version: 1.0 (MVP)
