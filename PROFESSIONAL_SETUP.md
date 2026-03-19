# 🚀 PROFESSIONAL SETUP GUIDE - Afya Yako AI

## Quick Start Commands

### Step 1: Database Setup
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Step 2: Create Admin User
```bash
python manage.py createsuperuser
```

When prompted:
- Username/Phone Number: Enter a phone number (e.g., +255712345678)
- Email: Enter your email
- Password: Create a strong password (minimum 8 characters)

### Step 3: Collect Static Files (Development)
```bash
python manage.py collectstatic --noinput
```

### Step 4: Run Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Access Points

Once the server is running at `http://localhost:8000`:

### 👤 Public Pages
- **Home Page**: `http://localhost:8000/` - Landing page with features overview
- **Login**: `http://localhost:8000/accounts/login/` - User login
- **Register**: `http://localhost:8000/accounts/register/` - New user registration

### 🔐 Protected Pages (Requires Login)
- **Dashboard**: `http://localhost:8000/accounts/dashboard/` - Main health dashboard
- **Profile**: `http://localhost:8000/accounts/profile/` - User profile management
- **Health Summary**: `http://localhost:8000/accounts/health-summary/` - Detailed health analytics

### 🔧 Admin Interface
- **Admin Panel**: `http://localhost:8000/admin/` - Django admin (use superuser credentials)

### 📱 API Endpoints (Authenticated)
All API endpoints are under `/accounts/api/`:

**Health Data APIs:**
- `/accounts/api/vitals/` - Blood pressure, heart rate, weight
- `/accounts/api/nutrition/` - Meal and calorie tracking
- `/accounts/api/exercises/` - Exercise and activity logging
- `/accounts/api/mood/` - Mood and emotional tracking
- `/accounts/api/sleep/` - Sleep tracking
- `/accounts/api/water/` - Water intake monitoring
- `/accounts/api/medications/` - Medication management
- `/accounts/api/appointments/` - Medical appointments
- `/accounts/api/blood-sugar/` - Blood sugar monitoring
- `/accounts/api/health-reports/` - Weekly health reports

---

## Professional Features

### 🎨 Modern Design System
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Professional Color Palette**: Blue-green gradient theme with accessible colors
- **Smooth Animations**: Subtle transitions and hover effects
- **Accessibility**: WCAG compliant, keyboard navigation support
- **Dark Mode Support**: Automatically adapts to system theme preference

### 🔐 Security Features
- **CSRF Protection**: Enabled on all forms
- **Session Security**: HTTP-only cookies, 2-week session timeout
- **Password Requirements**: Minimum 8 characters with strength indicator
- **User Authentication**: Phone number-based login system
- **Data Encryption**: Ready for HTTPS in production

### 📊 Admin Control Panel
The admin interface provides complete control over:

1. **User Management**
   - View all users with signup dates
   - Mark premium/active users
   - Reset passwords
   - Disable accounts

2. **Health Data Dashboard**
   - View all health metrics by user
   - Track vital signs trends
   - Monitor medication adherence
   - Check appointment schedules

3. **Customizable Filtering**
   - Filter by date, user, status
   - Search by phone number or name
   - Date hierarchy navigation (year → month → day)

4. **Bulk Actions**
   - Export data to CSV
   - Bulk status updates
   - User management tasks

---

## User Registration Flow

### 1. **Access Registration Page**
Navigate to `http://localhost:8000/accounts/register/`

### 2. **Fill Out Registration Form**
- **Personal Information**: Name, phone, email
- **Health Profile**: Age, gender, health focus area
- **Security**: Create password with strength indicator

### 3. **Form Validation**
- Phone number uniqueness check
- Password strength validation
- Password confirmation matching
- Age range validation (13-120)

### 4. **Account Creation**
- User profile automatically created
- Health tracking enabled
- Dashboard access granted

### 5. **Login**
Use phone number + password to login

---

## User Login Flow

### 1. **Access Login Page**
Navigate to `http://localhost:8000/accounts/login/`

### 2. **Enter Credentials**
- Phone number (as registered)
- Password
- Optional: Remember me checkbox

### 3. **Post-Login Experience**
Users see:
- **Quick Stats**: Latest vitals, mood, sleep duration
- **Health Alerts**: BP warnings, achievement celebrations
- **Dashboard Sections**:
  - Today's Metrics (steps, water, vitals)
  - Health Goals with progress bars
  - Upcoming Medical Appointments
  - AI Recommendations
  - Weekly Health Reports

---

## Dashboard Components

### 📈 Quick Stats Cards
Display latest measurements:
- Weight
- Mood Score
- Sleep Duration
- Pending Medications

### ⚠️ Health Alerts
Context-aware alerts for:
- High blood pressure warnings
- Good health celebrations
- Weekly report notifications
- Critical health indicators

### 🎯 Health Goals
Track progress on:
- Daily steps (target: 10,000)
- Water intake (target: 2,000ml)
- Sleep duration (target: 8 hours)
- Exercise minutes

### ⚡ Quick Actions
Fast access buttons to:
- Record vitals
- Log nutrition
- Record exercise
- Track mood
- Log sleep
- Manage medications

### 💡 AI Recommendations
Personalized health tips:
- Nutrition guidance
- Exercise suggestions
- Mental wellness tips

### 📅 Medical Appointments
View upcoming appointments with:
- Appointment type
- Location
- Date and time

---

## Admin Panel Features

### 👥 User Administration
```
Path: /admin/ → Users
```
- View all registered users
- Check user status (Admin, Premium, Active)
- Manage permissions
- View signup dates and login history
- Filter by premium status or active status

### 💊 Health Data Management
```
Path: /admin/ → Health Vitals/Nutrition/Exercise/Mood/etc.
```
- View all user health entries
- Filter by date range
- Search by user phone number
- Export data to CSV
- Edit or delete entries

### 💬 Medication Management
```
Path: /admin/ → Medications
```
- Track medication adherence
- View medication reminders
- Manage appointment schedules

### 📊 Reports
```
Path: /admin/ → Health Reports
```
- View generated weekly health reports
- Check AI recommendations by user
- Track health risk identification

---

## API Testing

### Using cURL
```bash
# Get user vitals (authenticated)
curl -H "Cookie: sessionid=<your-session-id>" \
     http://localhost:8000/accounts/api/vitals/

# Create new vital entry
curl -X POST http://localhost:8000/accounts/api/vitals/ \
     -H "Content-Type: application/json" \
     -H "Cookie: sessionid=<your-session-id>" \
     -d '{
       "weight": 75.5,
       "height": 175,
       "blood_pressure_systolic": 120,
       "blood_pressure_diastolic": 80,
       "heart_rate": 72
     }'
```

### Using Postman
1. Open Postman
2. Set base URL: `http://localhost:8000`
3. Login first to get session cookie
4. Add endpoints: `/accounts/api/vitals/`, `/accounts/api/nutrition/`, etc.
5. Send GET/POST requests with appropriate body

### Using Python Requests
```python
import requests

session = requests.Session()

# Login
login_data = {'phone': '+255712345678', 'password': 'yourpassword'}
session.post('http://localhost:8000/accounts/login/', data=login_data)

# Get vitals
response = session.get('http://localhost:8000/accounts/api/vitals/')
print(response.json())
```

---

## Customization Guide

### 1. **Change App Theme**
Edit `/static/css/professional.css`:
```css
--primary-blue: #YOUR_COLOR;
--primary-green: #YOUR_COLOR;
```

### 2. **Modify Admin Site Title**
Edit `/accounts/admin.py`:
```python
admin.site.site_header = "Your App Name"
admin.site.site_title = "Your Title"
```

### 3. **Add New Health Metrics**
1. Create model in `/accounts/models.py`
2. Create serializer in `/accounts/serializers.py`
3. Create ViewSet in `/accounts/views.py`
4. Register in admin at `/accounts/admin.py`
5. Add route in `/accounts/urls.py`

### 4. **Customize Dashboard**
Edit `/templates/accounts/dashboard.html`:
- Add/remove dashboard sections
- Modify card layouts
- Change icon selections
- Adjust color schemes

---

## Troubleshooting

### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'rest_framework'`

**Solution**:
```bash
pip install djangorestframework django-cors-headers
```

### Database Errors
**Problem**: `django.db.utils.OperationalError: no such table`

**Solution**:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
**Problem**: CSS/images not displaying

**Solution**:
```bash
python manage.py collectstatic --noinput
```

### Admin Login Issues
**Problem**: Can't login to admin

**Solution**:
```bash
python manage.py createsuperuser
# Create a new superuser account
```

### Authentication Required Error
**Problem**: API returns 401 Unauthorized

**Solution**:
- Ensure you're logged in before accessing protected pages
- Check session cookie is set
- Verify user is active (is_active=True)

---

## Performance Tips

1. **Enable Database Connection Pooling** (Production)
```python
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,
    }
}
```

2. **Use Caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

3. **Optimize Queries**
- Use `.select_related()` for foreign keys
- Use `.prefetch_related()` for reverse relations
- Add database indexes on frequently filtered fields

---

## Production Deployment Checklist

Before going live:
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Set up HTTPS/SSL certificates
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure Redis for caching
- [ ] Set up proper logging
- [ ] Enable CORS for production domain
- [ ] Run security checks: `python manage.py check --deploy`
- [ ] Create backup strategy
- [ ] Set up monitoring and alerts

---

## Support & Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **Font Awesome Icons**: https://fontawesome.com/

---

**Version**: 1.0  
**Last Updated**: January 30, 2026  
**Status**: Production Ready ✅
