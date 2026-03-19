# Menstrual Cycle Tracker - System Architecture

## System Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    MENSTRUAL CYCLE TRACKER                      │
│                        (Complete System)                        │
└─────────────────────────────────────────────────────────────────┘

                         ┌──────────────────┐
                         │  User (Django)   │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Web Browser  │  │  Mobile App  │  │  API Client  │
        │   (HTML/CSS) │  │  (Responsive)│  │   (JSON)     │
        └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
               │                 │                  │
               └─────────────────┼──────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Django URL Router     │
                    │  (menstrual/urls.py)    │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
      ┌────────▼────────┐  ┌─────▼──────┐  ┌──────▼──────┐
      │  Views Layer    │  │ Middleware │  │  Auth Check │
      │(views.py)       │  │  (CSRF)    │  │  @login_req │
      └────────┬────────┘  └─────┬──────┘  └──────┬──────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 │
      ┌──────────────────────────▼─────────────────────────┐
      │              API ENDPOINTS (8 Routes)              │
      ├──────────────────────────────────────────────────┤
      │ POST   /api/profile/setup/      → Create profile │
      │ GET    /api/profile/            → Get profile    │
      │ GET    /api/cycle-info/         → Today's data   │
      │ POST   /api/log/                → Log symptoms   │
      │ GET    /api/logs/?days=N        → History        │
      │ GET    /api/cycle-diagram/      → SVG data       │
      │ GET    /api/guidance/           → AI guidance    │
      │ GET    /api/insights/           → Patterns       │
      └──────────────────────────────────────────────────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 │
      ┌──────────────────────────▼──────────────────────┐
      │          Business Logic Layer                    │
      ├─────────────────────────────────────────────────┤
      │  menstrual/cycle_engine.py (300+ lines)         │
      │  ├─ get_cycle_day()      [1-indexed]           │
      │  ├─ get_phase()          [4 phases]            │
      │  ├─ get_fertility()      [high/med/low]        │
      │  ├─ generate_guidance()  [Gemini AI]           │
      │  ├─ detect_patterns()    [Analysis]            │
      │  └─ get_stats()          [Aggregation]         │
      └──────────────────────────────────────────────────┘
               │                 │
               └─────────────────┼─────────────────────┐
                                 │                     │
              ┌──────────────────▼─┐        ┌──────────▼────────┐
              │  Database Models    │        │  Google Gemini AI │
              │  (menstrual/        │        │  (gemini-2.5-    │
              │   models.py)        │        │   flash model)    │
              ├────────────────────┤        └───────────────────┘
              │ MenstrualProfile   │
              │  - user (1:1)      │
              │  - last_period     │
              │  - avg_cycle_len   │
              │  - pregnancy_goal  │
              ├────────────────────┤
              │ CycleDay           │
              │  - user (N:1)      │
              │  - date (unique)   │
              │  - cycle_day_num   │
              │  - phase           │
              │  - fertility_level │
              ├────────────────────┤
              │ DailyLog           │
              │  - user (N:1)      │
              │  - date (unique)   │
              │  - bleeding_level  │
              │  - pain_score      │
              │  - mood            │
              │  - symptoms (JSON) │
              │  - notes           │
              ├────────────────────┤
              │ CycleInsight       │
              │  - user (N:1)      │
              │  - insight_type    │
              │  - title           │
              │  - description     │
              └────────────────────┘
```

---

## Frontend Architecture

```
┌─────────────────────────────────────────────────────┐
│           Frontend Layer (Templates)                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  cycle_dashboard.html (MAIN PAGE)                  │
│  ├─ Navigation Bar                                 │
│  │  └─ Links: Dashboard, Chat, Cycle, Logout      │
│  │                                                 │
│  ├─ Section 1: Circular Cycle Diagram             │
│  │  ├─ SVG rendering (28 segments)                │
│  │  ├─ Color-coded by phase                       │
│  │  ├─ Current day highlighted                    │
│  │  └─ Interactive hover                          │
│  │                                                 │
│  ├─ Section 2: Status Widgets (4 cards)           │
│  │  ├─ Current Day + Phase                        │
│  │  ├─ Fertility Level                            │
│  │  ├─ Next Period Estimate                       │
│  │  └─ Quick action buttons                       │
│  │                                                 │
│  ├─ Section 3: Daily Logger Form                  │
│  │  ├─ Bleeding Level (5 buttons)                 │
│  │  ├─ Pain Score (slider 0-5)                   │
│  │  ├─ Mood (5 emoji buttons)                    │
│  │  ├─ Notes (textarea)                          │
│  │  └─ Submit button                              │
│  │                                                 │
│  ├─ Section 4: Charts & Graphs                    │
│  │  ├─ Bleeding Intensity (bar chart)             │
│  │  ├─ Pain Scores (line chart)                  │
│  │  └─ Mood Tracking (line chart)                │
│  │                                                 │
│  ├─ Section 5: Insights & Alerts                  │
│  │  ├─ Automatic pattern detection                │
│  │  ├─ Color-coded alerts                        │
│  │  └─ Health recommendations                     │
│  │                                                 │
│  └─ JavaScript Functions:                         │
│     ├─ loadCycleData()          [Fetch API]       │
│     ├─ renderCycleDiagram()     [SVG]             │
│     ├─ loadHistoryGraphs()      [Chart.js]        │
│     ├─ selectBleeding()         [Form handling]   │
│     ├─ selectMood()             [Form handling]   │
│     └─ submitDailyLog()         [API POST]        │
│                                                     │
│  setup.html (ONBOARDING PAGE)                      │
│  ├─ Title & Description                          │
│  ├─ Health Disclaimer                            │
│  ├─ Form fields:                                  │
│  │  ├─ Last period date (date picker)            │
│  │  ├─ Cycle length (number input)               │
│  │  ├─ Period length (number input)              │
│  │  ├─ Pregnancy goal (dropdown)                 │
│  │  └─ Submit button                             │
│  └─ Form validation & submission                  │
│                                                     │
└─────────────────────────────────────────────────────┘
        │                           │
        ▼                           ▼
    HTML Forms              JavaScript Event Listeners
        │                           │
        └───────────────┬───────────┘
                        │
           ┌────────────▼───────────┐
           │  Chart.js Integration  │
           ├────────────────────────┤
           │ • Bleeding bar chart   │
           │ • Pain line chart      │
           │ • Mood line chart      │
           │ • Responsive layout    │
           └────────────────────────┘
```

---

## Data Flow Diagram

```
NEW USER FLOW:
─────────────

1. User arrives at /menstrual/
   ↓
2. No profile exists → Redirect to setup.html
   ↓
3. User fills onboarding form
   ↓
4. POST to /api/profile/setup/
   ↓
5. Views → Create MenstrualProfile
   ↓
6. cycle_engine.generate_cycle_data() → Generate CycleDay records (180 days)
   ↓
7. Redirect to /menstrual/ (dashboard)
   ↓
8. cycle_dashboard.html loaded
   ↓
9. JavaScript fetches cycle data & renders UI
   ↓
10. User sees circular diagram, status cards, logger form


DAILY LOGGING FLOW:
──────────────────

1. User on cycle_dashboard.html
   ↓
2. Fills out daily logger form:
   - Select bleeding level (button click)
   - Adjust pain slider
   - Select mood emoji
   - Add notes (optional)
   ↓
3. Click "Save Today's Log"
   ↓
4. JavaScript → POST to /api/log/
   ↓
5. Views → Save DailyLog record
   ↓
6. API returns success
   ↓
7. JavaScript → Reload graphs & insights
   ↓
8. User sees updated charts


PATTERN ANALYSIS FLOW:
─────────────────────

1. User loads insights section
   ↓
2. JavaScript → GET /api/insights/
   ↓
3. Views → detect_cycle_patterns()
   ↓
4. cycle_engine analyzes past 60 days of logs:
   - Check for heavy bleeding (>10 days?)
   - Check for pain pattern (≥4 pain scores ≥4/5?)
   - Check for mood pattern (≥5 sad logs?)
   ↓
5. Generate CycleInsight records for any patterns
   ↓
6. API returns insights array
   ↓
7. JavaScript renders insight cards
   ↓
8. User sees pattern analysis & recommendations


AI GUIDANCE FLOW:
────────────────

1. User on cycle_dashboard or wants guidance
   ↓
2. JavaScript → GET /api/guidance/
   ↓
3. Views → cycle_engine.get_daily_guidance()
   ↓
4. get_daily_guidance():
   - Get user's MenstrualProfile
   - Calculate today's cycle day
   - Get today's phase
   - Get today's fertility level
   - Get today's DailyLog (if exists)
   ↓
5. Build prompt with all cycle context
   ↓
6. Send to Google Gemini AI (gemini-2.5-flash)
   ↓
7. Gemini generates personalized guidance:
   - Phase-specific expectations
   - Recommended exercise
   - Nutrition tips
   - Self-care suggestion
   - Fertility-aware messaging
   ↓
8. Save as CycleInsight (daily_guidance type)
   ↓
9. API returns guidance text
   ↓
10. JavaScript displays guidance to user


GRAPH RENDERING FLOW:
────────────────────

1. cycle_dashboard.html loads
   ↓
2. JavaScript calls loadHistoryGraphs()
   ↓
3. Fetch GET /api/logs/?days=90
   ↓
4. Views → Get DailyLog records for past 90 days
   ↓
5. Transform data:
   - Map bleeding_level → numeric (none=0, heavy=4)
   - Extract pain_score values
   - Convert mood → score (sad=1, happy=4)
   ↓
6. Format for Chart.js:
   - labels: [dates...]
   - datasets: [{label, data, color...}]
   ↓
7. Return JSON
   ↓
8. JavaScript creates 3 Chart.js instances:
   - Bleeding bar chart
   - Pain line chart
   - Mood line chart
   ↓
9. Charts render on page
```

---

## Cycle Calculation Algorithm

```
CYCLE PHASE CALCULATION:
─────────────────────────

Input: cycle_day_number (1-indexed, e.g., 14/28)

Process:
    if 1 ≤ cycle_day ≤ avg_period_length:
        phase = "menstrual"
        
    elif cycle_day ≤ avg_cycle_length * 0.46:
        phase = "follicular"
        
    elif cycle_day ≤ avg_cycle_length * 0.50:
        phase = "ovulation"
        
    else:
        phase = "luteal"

Example (28-day cycle):
    Days 1-5:   MENSTRUAL (5 days)
    Days 6-13:  FOLLICULAR (8 days) ← 46% of 28
    Day 14:     OVULATION (1 day)    ← 50% of 28
    Days 15-28: LUTEAL (14 days)     ← remainder


FERTILITY CALCULATION:
──────────────────────

high_start = avg_cycle_length * 0.36  # Day 10 for 28-day
high_end = avg_cycle_length * 0.54    # Day 15 for 28-day

if high_start ≤ cycle_day ≤ high_end:
    fertility = "high"
    
elif (high_start - 2) ≤ cycle_day ≤ (high_end + 2):
    fertility = "medium"
    
else:
    fertility = "low"

Example (28-day cycle):
    High fertility:   Days 10-15 (6 days peak)
    Medium fertility: Days 8-9, 16-17 (4 days buffer)
    Low fertility:    Days 1-7, 18-28 (18 days)


NEXT PERIOD CALCULATION:
────────────────────────

today_date = current date
last_period_start = stored baseline date
avg_cycle_length = user's cycle length (e.g., 28)

days_since_last = (today_date - last_period_start).days
current_cycle_number = days_since_last // avg_cycle_length
cycle_end_date = last_period_start + (
    (current_cycle_number + 1) * avg_cycle_length days
)

next_period_date = cycle_end_date

Example:
    last_period = 2024-02-10
    today = 2024-03-10 (28 days later)
    next period = 2024-03-10 (today!) = Day 1
    
    If today = 2024-02-20 (10 days after):
    days_since = 10
    cycle_num = 10 // 28 = 0
    cycle_end = 2024-02-10 + 28 = 2024-03-10
    next_period = 2024-03-10 (18 days away)
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────┐
│         Error Handling Strategy         │
└─────────────────────────────────────────┘

AUTHENTICATION ERRORS:
  User not logged in
     ↓
  @login_required decorator
     ↓
  Redirect to /login/

MISSING PROFILE:
  GET /api/cycle-info/ before setup
     ↓
  MenstrualProfile.DoesNotExist exception
     ↓
  API returns: {"error": "Profile not found. Setup required."}
     ↓
  Status: 404
     ↓
  Frontend redirects to setup page

INVALID REQUEST DATA:
  POST /api/log/ with invalid date format
     ↓
  ValueError in datetime.strptime()
     ↓
  try/except catches it
     ↓
  API returns: {"error": "Invalid date format"}
     ↓
  Status: 400

API REQUEST ERRORS:
  GET /api/guidance/ fails (Gemini timeout)
     ↓
  exception in get_daily_guidance()
     ↓
  Returns: {"error": "Could not generate guidance"}
     ↓
  Frontend shows fallback message

FORM VALIDATION:
  Daily logger with missing mood
     ↓
  JavaScript validates form before POST
     ↓
  If invalid, shows alert
     ↓
  If valid, submits to API
     ↓
  API validates again (server-side)
     ↓
  If error, returns error message
     ↓
  Frontend displays alert

CSRF PROTECTION:
  POST request without CSRF token
     ↓
  Django CSRF middleware intercepts
     ↓
  Returns: 403 Forbidden
     ↓
  Frontend ensures CSRF token in every POST
```

---

## Performance Optimization

```
QUERY OPTIMIZATION:
─────────────────────
• MenstrualProfile: Indexed on user_id (OneToOne is unique)
• CycleDay: Indexed on (user_id, date) - unique_together
• DailyLog: Indexed on (user_id, date) - unique_together
• Uses select_related() for FK queries
• Limits to 90-day window for graphs

CACHING STRATEGY:
─────────────────
• CycleDay records pre-generated (180 days) for fast lookup
• No need to recalculate cycle info on each request
• Simple filter: CycleDay.objects.get(user=user, date=today)

FRONTEND OPTIMIZATION:
──────────────────────
• Single JavaScript bundle (no framework bloat)
• SVG diagram rendered once on page load
• Charts only recreated when data changes
• Async API calls don't block UI
• Mobile-first CSS prevents unnecessary redraws

RESPONSE OPTIMIZATION:
──────────────────────
• API returns minimal JSON (no nested objects)
• Logs endpoint supports ?days=N pagination
• Frontend handles 60+ days of chart data smoothly
```

---

## Security Model

```
┌──────────────────────────────────────────┐
│      Security Layers (Defense-in-Depth)  │
└──────────────────────────────────────────┘

LAYER 1: AUTHENTICATION
  ├─ @login_required on all views
  ├─ User must be logged in
  └─ Session cookie verification

LAYER 2: AUTHORIZATION
  ├─ User can only see own data
  ├─ Query filter: .filter(user=request.user)
  ├─ No cross-user data leaks
  └─ Admin panel restricted to staff

LAYER 3: CSRF PROTECTION
  ├─ CSRF token required on all POST/PUT/DELETE
  ├─ Token validated by middleware
  ├─ Frontend includes token in requests
  └─ Returns 403 if missing or invalid

LAYER 4: INPUT VALIDATION
  ├─ Server-side validation on all inputs
  ├─ Type checking (int, date, enum)
  ├─ Range validation (pain 0-5, cycle 20-45)
  ├─ SQL injection prevention via ORM
  └─ XSS prevention via template escaping

LAYER 5: DATA ENCRYPTION
  ├─ HTTPS recommended in production
  ├─ Passwords hashed with Django's hasher
  ├─ No sensitive data in logs
  └─ Session data server-side only

LAYER 6: API RATE LIMITING
  ├─ Can be added with throttle_classes
  ├─ Prevent abuse (e.g., 100 requests/hour)
  ├─ IP-based or user-based limits
  └─ Returns 429 if exceeded
```

---

## Deployment Checklist

```
✅ PRE-DEPLOYMENT
  ☐ Run: python manage.py check --deploy
  ☐ Update: DEBUG = False
  ☐ Set: ALLOWED_HOSTS = ['yourdomain.com']
  ☐ Configure: HTTPS/SSL certificates
  ☐ Set: SECRET_KEY (strong, random)
  ☐ Configure: CSRF_TRUSTED_ORIGINS
  ☐ Set: EMAIL backend (for notifications)
  ☐ Configure: Database (PostgreSQL recommended)
  ☐ Set: Google Gemini API key
  ☐ Run: python manage.py collectstatic

✅ DATABASE
  ☐ Run migrations: python manage.py migrate
  ☐ Create superuser: python manage.py createsuperuser
  ☐ Backup existing data
  ☐ Verify migrations completed successfully

✅ MONITORING
  ☐ Set up error logging (Sentry/NewRelic)
  ☐ Configure email alerts
  ☐ Monitor API response times
  ☐ Track user signup rates

✅ TESTING
  ☐ Test profile setup flow
  ☐ Test daily logging
  ☐ Test API endpoints
  ☐ Test charts rendering
  ☐ Test mobile responsiveness
  ☐ Test on production database
```

---

This architecture supports scaling to thousands of users while maintaining security and performance.
