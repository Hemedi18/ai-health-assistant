# Menstrual Cycle Tracker - Quick Start Guide

## Setup in 5 Minutes

### 1. Create a Test User (Django Shell)
```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.create_user(
    u_phone_number='255123456789',
    password='testpass123'
)
print(f"✓ User created: {user.u_phone_number}")
```

### 2. Set Up Menstrual Profile
**Option A: Via Web UI**
1. Log in at `/accounts/login/`
2. You'll be redirected to menstrual setup page
3. Fill in:
   - Last period start date: e.g., 2024-02-10
   - Average cycle length: 28 days (default)
   - Average period length: 5 days (default)
   - Pregnancy goal: Choose one
4. Click "Start Tracking"

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/menstrual/api/profile/setup/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -d '{
    "last_period_start": "2024-02-10",
    "avg_cycle_length": 28,
    "avg_period_length": 5,
    "pregnancy_goal": "track"
  }'
```

### 3. Access the Dashboard
- Go to: `http://localhost:8000/menstrual/`
- You'll see:
  - Circular cycle diagram (center shows current day)
  - Status cards (current phase, fertility, next period)
  - Daily logger form
  - Tracking graphs
  - Insights & alerts

### 4. Log Today's Data
1. Scroll to "Today's Log" section
2. Select bleeding level (None, Spotting, Light, Medium, Heavy)
3. Adjust pain slider (0-5)
4. Choose a mood emoji
5. Add notes (optional)
6. Click "Save Today's Log"

### 5. View Cycle Information
**Via Web:**
- Click "Track Cycle" button on main dashboard
- Visual circular diagram shows all 28 days
- Current day highlighted with glow

**Via API:**
```bash
curl http://localhost:8000/menstrual/api/cycle-info/
```

Returns:
```json
{
  "today": "2024-03-10",
  "cycle_day": 14,
  "phase": "ovulation",
  "phase_name": "Ovulation",
  "fertility_level": "high",
  "next_period": "2024-03-25"
}
```

## Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/menstrual/api/profile/setup/` | Initialize profile |
| GET | `/menstrual/api/profile/` | Get profile info |
| GET | `/menstrual/api/cycle-info/` | Get today's cycle data |
| POST | `/menstrual/api/log/` | Log daily data |
| GET | `/menstrual/api/logs/?days=90` | Get past logs |
| GET | `/menstrual/api/cycle-diagram/` | Get diagram data |
| GET | `/menstrual/api/guidance/` | Get AI guidance |
| GET | `/menstrual/api/insights/` | Get pattern insights |

## Features Walkthrough

### Circular Cycle Diagram
```
             Day 1
          ↙      ↘
       Menstrual  Follicular
    (Red)          (Pink)
       ↖      ↗
      Day 14 (Ovulation - Green)

      Luteal (Purple) - Days 15-28
```

- Click/hover any day to see details
- Red = Menstrual phase
- Pink = Follicular (building up)
- Green = Ovulation (fertile window)
- Purple = Luteal (winding down)

### Fertility Tracking
- **High Fertility** (Days 10-15): Perfect time if trying to conceive
- **Medium Fertility**: Plus/minus 2 days from high window
- **Low Fertility**: Lower probability of conception

### Daily Logging Options

| Field | Options |
|-------|---------|
| Bleeding | None, Spotting, Light, Medium, Heavy |
| Pain | 0-5 scale (slider) |
| Mood | 😊 Happy, 😐 Neutral, 😢 Sad, 😰 Anxious, 😠 Irritable |
| Notes | Free text (optional) |

### Charts & Graphs

**Bleeding Intensity Chart**
- Bar chart of bleeding levels over time
- Helps identify patterns
- Red color indicates bleeding days

**Pain Score Chart**
- Line graph of pain levels
- Helps track if pain is improving/worsening
- Orange line with area fill

**Mood Chart**
- Line graph of mood trends
- Purple line
- Useful for PMS pattern detection

### AI Guidance
Click the daily guidance card to see:
- Phase-specific insights (what to expect today)
- Recommended exercise type
- Nutrition tips
- Self-care suggestion
- Fertility-aware advice

Example for Ovulation Day:
```
Today you're in the Ovulation phase (Day 14/28)
Energy: Peak
Mood: Energetic and confident

Recommendations:
- Exercise: Intense workouts perfect today! High energy ideal for strength training or HIIT
- Nutrition: Increase protein intake, stay hydrated
- Self-care: Channel your energy into projects/socializing
- Fertility: High fertility window - Important if tracking pregnancy
```

### Pattern Insights
System automatically detects:
- Heavy or extended bleeding
- Consistent menstrual pain
- Mood changes during cycle
- Cycle irregularities

Example alert:
```
⚠️ Significant menstrual pain noted
You've logged pain levels of 4+. OTC pain relief or a 
warm compress may help. Consult a provider if severe.
```

## Navigation

### From Main Dashboard
1. Dashboard has menstrual widget (if profile exists)
2. Click "Track Cycle" button → Goes to `/menstrual/`
3. Click "Log Today" button → Scrolls to daily logger

### Top Navigation Bar
- Logo → Dashboard
- 💬 Chat → Chat AI
- 🩸 Cycle → Menstrual Tracker
- Logout → Sign out

## Admin Management

Access at `/admin/`:
1. Go to Menstrual section
2. View/edit:
   - Menstrual Profiles (user baseline data)
   - Cycle Days (calculated daily info)
   - Daily Logs (user entries)
   - Cycle Insights (AI-generated guidance)

## Troubleshooting

### "Profile not found" Error
- User hasn't completed setup yet
- Click "Start Tracking" and fill out onboarding form
- Then refresh the page

### Charts Not Showing
- Need at least 2 weeks of logged data
- Keep logging for data to accumulate
- Check if logs have `bleeding_level` or `pain_score` values

### AI Guidance Not Loading
- Check internet connection
- Verify Google Gemini API key in environment
- Check Django logs for errors

### Widget Not on Dashboard
- Make sure user is logged in
- Complete menstrual profile setup
- Hard refresh page (Ctrl+Shift+R)

## Example Workflow

### Day 1 - First Period
1. Open `/menstrual/`
2. Day will show as "Day 1 - Menstrual"
3. Log: Bleeding (Heavy), Pain (4/5), Mood (Sad)
4. System shows: Low energy expected, gentle exercises recommended

### Day 14 - Ovulation
1. Dashboard shows "Day 14 - Ovulation"
2. Fertility badge shows "High"
3. AI guidance: Peak energy, great time for intense workouts
4. If trying to conceive: This is optimal time

### Day 21 - Luteal Phase
1. Shows "Day 21 - Luteal"
2. Energy drops, mood may shift
3. AI suggests: Gentle yoga, extra sleep, magnesium-rich foods
4. If PMS symptoms detected: Recommendations provided

### Day 28 - End of Cycle
1. Last day before period restarts
2. System predicts next period: ~3 days away
3. If late: App will note irregular cycle

## Next Steps After Setup

1. **Log Daily for 2-3 Cycles**: Better patterns emerge with more data
2. **Review Insights**: Check back weekly for pattern analysis
3. **Share with Provider** (future feature): Export reports for doctor
4. **Adjust Baseline**: If cycle length changes, update in profile

## Important Reminders

⚠️ **This App Is For Tracking Only:**
- NOT a replacement for medical care
- NOT a contraceptive method (if using for avoidance, also use protection)
- NOT diagnostic - always consult a doctor for concerns
- NOT for emergencies - call emergency services if needed

✅ **Best Practices:**
- Log consistently for accurate insights
- Be honest about symptoms
- Update profile if cycle changes
- Consult healthcare provider for irregular patterns

## Getting Help

**In-app**: Check "Insights" section for tips
**Docs**: See `MENSTRUAL_TRACKER_DOCS.md` for full documentation
**API**: Use `/api/` endpoints for custom integrations

---

**Ready to start tracking?** Log in and set up your profile now! 🩸
