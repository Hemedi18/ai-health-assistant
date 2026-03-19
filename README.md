# Afya Yako AI - Health Management System 🏥

A comprehensive AI-powered health management application for Tanzania and beyond.

## Overview

Afya Yako AI is a personal health management system that enables users to:

- **Track Health Data**: Vitals, nutrition, exercise, mental health
- **Receive AI Recommendations**: Personalized health tips based on profile
- **Manage Medications**: Track medications, set reminders, monitor adherence
- **Schedule Appointments**: Organize doctor appointments and medical visits
- **Get Health Insights**: Weekly reports with risk identification and recommendations
- **Chat with AI Health Assistant**: Ask health questions for education

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Django 4.2+
- pip package manager

### Installation

1. **Clone/Setup Project**
```bash
cd /home/hacker/Desktop/health_project
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create Superuser**
```bash
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

## 📋 Features

### Core Modules

#### 1. **Health Vitals Tracking** 💉
- Weight, Height, BMI (auto-calculated)
- Blood Pressure (Systolic/Diastolic)
- Heart Rate
- Weekly averages and trends
- Visual health dashboard

#### 2. **Nutrition Management** 🍎
- Log meals (breakfast, lunch, dinner, snacks)
- Track calories and macronutrients
- Set daily nutrition goals
- Water intake logging
- Special diet support (diabetic, low-salt, etc.)

#### 3. **Physical Activity** 🏃
- Exercise tracking with intensity levels
- Daily step counting
- Calories burned calculation
- Weekly activity summaries
- Fitness goal setting

#### 4. **Mental Health & Wellness** 🧠
- Daily mood tracking
- Sleep duration and quality monitoring
- Stress and anxiety levels
- Mindfulness activities (meditation, yoga, breathing)
- Mental health trends analysis

#### 5. **Medication Management** 💊
- Add and track medications
- Set medication reminders
- Monitor medication adherence
- Track side effects
- Medical appointment scheduling

#### 6. **Blood Sugar Monitoring** 🩸
- Log blood sugar readings
- Fasting and postprandial tracking
- Weekly averages
- For diabetes management

#### 7. **AI-Powered Features** 🤖
- **Health Summary**: Comprehensive profile analysis
- **Personalized Tips**: AI-generated health recommendations
- **Nutrition Advice**: Local Tanzanian food recommendations
- **Exercise Plans**: Customized workout recommendations
- **Wellness Tips**: Mental health guidance
- **Health Q&A**: Educational health chatbot
- **Smart Reports**: Weekly health analysis with insights

#### 8. **Health Reports** 📊
- Weekly health summaries
- Risk identification
- Personalized recommendations
- Progress tracking
- Trend analysis

## 🔐 Safety & Compliance

### Health Disclaimers
- ⚠️ App is for tracking and education only, NOT medical diagnosis
- Always consult healthcare professionals
- Emergency red-flag detection
- Clear guidance on when to seek medical attention

### Data Security
- User authentication required
- Data encryption ready (can be enabled)
- CSRF protection
- Secure password hashing

### Privacy
- User consent management
- Privacy policy included
- Data usage guidelines
- Compliance checklists

## 📱 API Endpoints

### Authentication Required Endpoints

**Health Vitals**
- `GET /api/vitals/` - List all vitals
- `POST /api/vitals/` - Log new vital signs
- `GET /api/vitals/latest/` - Get latest vitals
- `GET /api/vitals/weekly_average/` - Get weekly averages

**Nutrition**
- `POST /api/nutrition/` - Log meal
- `GET /api/nutrition/today_summary/` - Today's nutrition
- `POST /api/water/` - Log water intake
- `GET /api/water/today_total/` - Daily water intake

**Exercise**
- `POST /api/exercises/` - Log exercise
- `GET /api/exercises/weekly_summary/` - Weekly summary
- `POST /api/steps/` - Log steps
- `GET /api/steps/` - Get step records

**Mental Health**
- `POST /api/mood/` - Log mood
- `GET /api/mood/weekly_trends/` - Mood trends
- `POST /api/sleep/` - Log sleep
- `GET /api/sleep/weekly_average/` - Sleep average

**Medications**
- `POST /api/medications/` - Add medication
- `GET /api/medications/active/` - Active medications
- `POST /api/appointments/` - Schedule appointment

**AI Features**
- `GET /chat-ai/api/health-summary/` - Health insights
- `GET /chat-ai/api/nutrition-advice/` - Nutrition tips
- `GET /chat-ai/api/wellness-tips/` - Wellness guidance
- `GET /chat-ai/api/exercise-recommendations/` - Exercise plans
- `POST /chat-ai/api/ask-question/` - Ask health questions
- `POST /chat-ai/api/send/` - Chat with AI

## 📊 Dashboard

The main dashboard includes:
- Quick health stats cards
- Latest vital signs
- Today's mood and sleep
- AI insights preview
- Health tracking features
- Medication management
- AI recommendations
- Educational resources
- Health goals progress

## 🎯 MVP Feature Set

**Included in v1.0:**
✅ User profiles with age & gender
✅ Daily health tracking
✅ Nutrition & exercise advice
✅ Mental well-being tracking
✅ AI personalized tips
✅ Safety disclaimers
✅ Health reports
✅ Medication management
✅ Appointment scheduling
✅ Emergency detection

**Future Enhancements:**
- Wearable device integration
- Telemedicine consultations
- Community features
- Advanced analytics
- Local clinic integration

## 🌍 Tanzanian Context

The app is optimized for Tanzania:
- Uses local currency and measurements
- Recommends local Tanzanian foods (ugali, beans, cassava, etc.)
- Considers local climate and lifestyle
- Emergency numbers for Tanzania (112)
- Supports Swahili (can be added)
- Healthcare system awareness

## 📚 Documentation

- **[API Documentation](API_DOCUMENTATION.md)** - Complete API endpoint reference
- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Setup and usage instructions
- **[Compliance Module](compliance_safety.py)** - Health disclaimers and safety protocols

## 🔧 Tech Stack

**Backend**
- Django 4.2
- Django REST Framework
- Google Gemini AI (for personalization)
- SQLite (development)

**Frontend**
- Bootstrap 5
- JavaScript
- Django Templates

**Services**
- Google GenAI API (for AI features)

## 🏥 Health Education Resources

The app includes information about:
- Balanced nutrition and local foods
- Age-appropriate exercise
- Managing chronic conditions
- Mental health awareness
- Reproductive health
- Preventive care

## ⚠️ Important Disclaimers

**THIS APP IS NOT:**
- A medical diagnosis tool
- A substitute for healthcare professionals
- Licensed to treat diseases
- A replacement for emergency services

**ALWAYS:**
- Consult healthcare professionals for medical concerns
- Seek emergency care for urgent issues
- Report serious symptoms to a doctor
- Use this as a supplement, not replacement

**EMERGENCY:** Call 112 (Tanzania) for emergencies

## 👥 User Management

### Admin Panel
Access admin panel at `/admin/`
- Manage users
- View health data
- Monitor app usage
- Generate reports

### User Roles
- **Free Users**: Basic health tracking
- **Premium Users**: All features (when implemented)

## 🔄 Data Flow

```
User Input → Validation → Database Storage → Analytics → AI Analysis → Recommendations
                                                      ↓
                                              Dashboard Display
                                                      ↓
                                              User Notifications
```

## 📈 Performance

- Optimized database queries
- Efficient API endpoints
- Caching for frequently accessed data (recommended)
- Scalable architecture

## 🐛 Known Issues

None currently. See [GitHub Issues](https://github.com/yourrepo/issues) for reporting.

## 🤝 Contributing

Contributions welcome! Please:
1. Create feature branch
2. Make changes
3. Submit pull request
4. Follow code style guidelines

## 📝 License

[Specify your license - MIT, GPL, etc.]

## 📞 Support

- Email: support@afyayakoai.tz
- Issues: GitHub Issues
- Documentation: See docs/ folder

## 🙏 Acknowledgments

- Google Gemini AI for personalization
- Django community
- Bootstrap for UI
- Tanzania Ministry of Health

## 📅 Roadmap

### v1.0 (Current) ✅
- Core health tracking
- Basic AI features
- Health reporting
- Medication management

### v1.1 (Planned)
- Wearable integration
- Enhanced analytics
- Community features
- Telemedicine beta

### v2.0 (Future)
- Full telemedicine
- Advanced ML models
- Multi-language support
- Insurance integration

## 🔐 Security Notes

For production deployment:
- Enable HTTPS
- Configure strong SECRET_KEY
- Use environment variables for sensitive data
- Set up database backups
- Enable logging and monitoring
- Regular security audits

## 📧 Contact

**Developer**: [Your Name/Organization]
**Email**: [Your Email]
**Website**: [Your Website]
**Location**: Tanzania

---

**Last Updated:** January 30, 2026
**Version:** 1.0 (MVP)
**Status:** Active Development

Thank you for using Afya Yako AI! 🌟
