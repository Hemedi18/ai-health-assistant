# Menstrual Cycle Tracking System

## Overview

The menstrual cycle tracking system is a comprehensive health feature that helps users monitor their menstrual health with AI-powered insights, daily logging, and predictive analytics.

## Features

### 1. **Cycle Dashboard** (`/menstrual/`)
- **Circular Diagram**: Visual 28-day cycle representation with color-coded phases
- **Current Status**: Display cycle day, phase, fertility level, and next period estimate
- **Daily Logging**: Quick form to track bleeding, pain, mood, and symptoms
- **Tracking History**: Line/bar charts showing bleeding intensity, pain scores, and mood patterns over 90 days
- **Insights & Alerts**: Pattern detection and personalized guidance

### 2. **Setup Wizard** (`/menstrual/setup/` - Auto-shown if profile missing)
- Collects baseline information:
  - Last period start date
  - Average cycle length (default: 28 days)
  - Average period length (default: 5 days)
  - Pregnancy goal (track/conceive/avoid)

### 3. **Cycle Calculations**
The system uses medical cycle science for accurate tracking:
- **Menstrual Phase**: Days 1-5 (or configurable)
- **Follicular Phase**: ~46% of cycle (e.g., days 6-13 for 28-day)
- **Ovulation Phase**: Day 14 (50% mark)
- **Luteal Phase**: Remainder (e.g., days 15-28)

### 4. **Fertility Tracking**
- **High Fertility**: Days 10-15 (36-54% of cycle) - 5 fertile days
- **Medium Fertility**: 2 days before/after high window
- **Low Fertility**: Other days
- Pregnancy goal-aware guidance

### 5. **Daily Logging**
Users can log:
- **Bleeding Level**: None, spotting, light, medium, heavy
- **Pain Score**: 0-5 scale for menstrual pain
- **Mood**: 5 emoji options (happy, neutral, sad, anxious, irritable)
- **Notes**: Free-text observations

### 6. **AI Guidance**
Powered by Google Gemini, generates daily personalized guidance including:
- Phase-specific energy expectations
- Recommended exercise types
- Nutrition tips (e.g., iron during menstrual, magnesium during luteal)
- Self-care suggestions
- Fertility-aware contraception/conception guidance

### 7. **Pattern Detection**
Analyzes logs for:
- Heavy/extended bleeding (alert if >10 days in 60 days)
- Significant menstrual pain (alert if ≥5 instances with pain ≥4/5)
- Mood patterns (PMS detection if ≥5 sad logs)
- Cycle irregularities

### 8. **Dashboard Integration**
Displays menstrual widget on main dashboard showing:
- Current cycle day
- Current phase
- Fertility level today
- Next period estimate
- Quick links to tracker

## Database Schema

### Models

#### `MenstrualProfile` (OneToOne with User)
```python
- user: OneToOneField(User)
- last_period_start: DateField
- avg_cycle_length: IntegerField (default: 28)
- avg_period_length: IntegerField (default: 5)
- pregnancy_goal: CharField (track/conceive/avoid)
```

#### `CycleDay` (Pre-calculated daily info)
```python
- user: ForeignKey(User)
- date: DateField (unique_together with user)
- cycle_day_number: IntegerField (1-indexed)
- phase: CharField (menstrual/follicular/ovulation/luteal)
- fertility_level: CharField (low/medium/high)
```

#### `DailyLog` (User daily tracking)
```python
- user: ForeignKey(User)
- date: DateField (unique_together with user)
- bleeding_level: CharField (none/spotting/light/medium/heavy)
- pain_score: IntegerField (0-5)
- mood: CharField
- symptoms: JSONField (list)
- notes: TextField
```

#### `CycleInsight` (AI-generated insights)
```python
- user: ForeignKey(User)
- insight_type: CharField (pattern/daily_guidance/alert)
- title: CharField
- description: TextField
- date: DateField
```

## API Endpoints

### Cycle Information
- `GET /menstrual/api/cycle-info/` - Get today's cycle data
- `GET /menstrual/api/cycle-diagram/` - Get 28-segment diagram data
- `GET /menstrual/api/profile/` - Get user's menstrual profile

### Profile Management
- `POST /menstrual/api/profile/setup/` - Initialize/update profile
- `GET /menstrual/api/profile/` - Get current profile

### Daily Tracking
- `POST /menstrual/api/log/` - Log daily data
- `GET /menstrual/api/logs/?days=90` - Get logs for past N days

### Guidance & Insights
- `GET /menstrual/api/guidance/` - Get AI-generated daily guidance
- `GET /menstrual/api/insights/` - Get pattern insights and alerts

## Frontend Components

### Circular Cycle Diagram
- SVG rendering with 28 color-coded segments
- Each segment represents one cycle day
- Current day highlighted with glow effect
- Hoverable for day details
- Shows bleating/pain/mood icons overlaid

### Daily Logger Form
- Radio buttons for bleeding level
- Slider for pain score (0-5)
- Emoji buttons for mood selection
- Text area for notes
- Submit button saves to database

### Charts (Chart.js)
- **Bleeding Intensity**: Bar chart (0-4 scale)
- **Pain Scores**: Line chart (0-5 scale)
- **Mood Tracking**: Line chart (mood value scores)
- All configurable for custom date ranges

### Status Cards
- Current cycle day and phase
- Today's fertility level
- Next period estimate
- Quick action buttons

## Security & Privacy

- ⚠️ **Non-Medical**: App provides tracking and guidance only, not medical diagnosis
- 🔒 **User Data**: All cycle data stored per-user, requires authentication
- 🛡️ **CSRF Protected**: All POST endpoints require CSRF token
- 📱 **Mobile-Optimized**: Fully responsive for all screen sizes

## Usage Examples

### Example 1: New User Setup
```javascript
// POST to /menstrual/api/profile/setup/
{
  "last_period_start": "2024-02-10",
  "avg_cycle_length": 28,
  "avg_period_length": 5,
  "pregnancy_goal": "track"
}

// Response
{
  "success": true,
  "message": "Profile setup complete",
  "profile": {
    "last_period_start": "2024-02-10",
    "avg_cycle_length": 28,
    "avg_period_length": 5,
    "pregnancy_goal": "track"
  }
}
```

### Example 2: Get Today's Info
```javascript
// GET /menstrual/api/cycle-info/
// Response
{
  "today": "2024-03-10",
  "cycle_day": 14,
  "cycle_length": 28,
  "phase": "ovulation",
  "phase_name": "Ovulation",
  "phase_color": "#44FF44",
  "fertility_level": "high",
  "next_period": "2024-03-25",
  "phase_info": {
    "name": "Ovulation",
    "energy": "Peak",
    "mood": "Energetic and confident",
    ...
  }
}
```

### Example 3: Log Daily Data
```javascript
// POST /menstrual/api/log/
{
  "date": "2024-03-10",
  "bleeding_level": "none",
  "pain_score": 2,
  "mood": "happy",
  "symptoms": ["bloating", "breast_tenderness"],
  "notes": "Feeling energetic, good workout today"
}
```

## Configuration

### Customize Cycle Phases
In `menstrual/models.py`, modify `get_cycle_phase()`:
```python
def get_cycle_phase(self, cycle_day):
    if 1 <= cycle_day <= self.avg_period_length:
        return 'menstrual'
    elif cycle_day <= int(self.avg_cycle_length * 0.46):
        return 'follicular'
    # ... etc
```

### Customize Phase Information
In `menstrual/cycle_engine.py`, update `PHASE_INFO` dict:
```python
PHASE_INFO = {
    'menstrual': {
        'name': 'Menstrual',
        'energy': 'Low to moderate',
        'mood': 'May experience mood changes',
        # ...
    }
}
```

### Customize Colors
In `menstrual/cycle_engine.py`, update `PHASE_COLORS`:
```python
PHASE_COLORS = {
    'menstrual': '#FF4444',
    'follicular': '#FFB6D9',
    'ovulation': '#44FF44',
    'luteal': '#9966CC',
}
```

## Troubleshooting

### Widget Not Showing on Dashboard
1. User must have a MenstrualProfile
2. Profile must have a valid `last_period_start` date
3. Check browser console for API errors
4. Verify user is authenticated

### Guidance Generation Fails
1. Ensure Google Gemini API key is set in `.env`
2. Check API rate limits
3. Review `menstrual/cycle_engine.py::get_daily_guidance()` for errors

### Charts Not Rendering
1. Ensure Chart.js is loaded (check CDN link)
2. Verify sufficient log data exists (need ≥2 weeks)
3. Check browser console for JavaScript errors

## Future Enhancements

- [ ] Period predictions with ML
- [ ] Integration with wearable devices
- [ ] Medication tracking (hormonal contraceptives)
- [ ] Pregnancy mode (cycle tracking → trimester tracking)
- [ ] Symptom severity scoring
- [ ] Sharing with healthcare providers (export)
- [ ] Community insights (aggregated, anonymized trends)
- [ ] Hormone level estimation (based on logs)
- [ ] Integration with calendar apps
- [ ] Reminder notifications for logging

## Testing

```bash
# Run tests
python manage.py test menstrual

# Test API endpoints
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/menstrual/api/cycle-info/

# Generate test data
python manage.py shell
>>> from menstrual.cycle_engine import generate_cycle_data
>>> from django.contrib.auth import get_user_model
>>> user = get_user_model().objects.first()
>>> generate_cycle_data(user, days_ahead=180)
```

## Dependencies

- Django 6.0.1+
- Django REST Framework 3.16.1+
- google-generativeai (deprecated, consider upgrading to google-genai)
- Chart.js 3.9.1+ (CDN)
- Bootstrap 5.3.0+ (CDN)

## File Structure

```
menstrual/
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
├── templates/
│   └── menstrual/
│       ├── cycle_dashboard.html    # Main tracker UI
│       └── setup.html              # Onboarding wizard
├── admin.py                        # Django admin configuration
├── apps.py                         # App configuration
├── cycle_engine.py                 # Cycle logic & AI guidance
├── models.py                       # Database models (4 models)
├── urls.py                         # URL routing (8 endpoints)
├── views.py                        # API views & rendering
└── tests.py                        # Unit tests (optional)
```

## Support & Disclaimer

This application provides **educational tracking and AI-powered guidance only**. It is **not a medical device** and should not be used for:
- Medical diagnosis
- Treatment recommendations
- Emergency situations

Always consult a healthcare provider for:
- Irregular bleeding patterns
- Severe pain
- Suspected pregnancy complications
- Any medical concerns

## License

Part of Afya Yako Health Project - Health Tracking System for Tanzania
