from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, HealthVitalViewSet, NutritionEntryViewSet,
    DailyNutritionGoalViewSet, WaterIntakeViewSet, ExerciseViewSet,
    DailyStepsViewSet, FitnessGoalViewSet, MoodEntryViewSet,
    SleepEntryViewSet, MindfulnessSessionViewSet, MedicationViewSet,
    MedicationAdherenceViewSet, MedicalAppointmentViewSet,
    BloodSugarEntryViewSet, HealthReportViewSet, dashboard_view
    , add_vital_view, add_nutrition_view, add_exercise_view,
    add_mood_view, add_sleep_view, add_medication_view
) # Added new form views
from .auth_views import (
    home_view, login_view, register_view, logout_view, 
    profile_view, health_summary_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'vitals', HealthVitalViewSet, basename='vital')
router.register(r'nutrition', NutritionEntryViewSet, basename='nutrition')
router.register(r'water', WaterIntakeViewSet, basename='water')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'steps', DailyStepsViewSet, basename='steps')
router.register(r'mood', MoodEntryViewSet, basename='mood')
router.register(r'sleep', SleepEntryViewSet, basename='sleep')
router.register(r'mindfulness', MindfulnessSessionViewSet, basename='mindfulness')
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'medication-adherence', MedicationAdherenceViewSet, basename='medication-adherence')
router.register(r'appointments', MedicalAppointmentViewSet, basename='appointment')
router.register(r'blood-sugar', BloodSugarEntryViewSet, basename='blood-sugar')
router.register(r'health-reports', HealthReportViewSet, basename='health-report')

urlpatterns = [
    # Authentication URLs
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('health-summary/', health_summary_view, name='health_summary'),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Form Views (User Interaction)
    path('vitals/', add_vital_view, name='add_vital'),
    path('add/nutrition/', add_nutrition_view, name='add_nutrition'),
    path('add/exercise/', add_exercise_view, name='add_exercise'),
    path('add/mood/', add_mood_view, name='add_mood'),
    path('add/sleep/', add_sleep_view, name='add_sleep'),
    path('add/medication/', add_medication_view, name='add_medication'),
    
    # API URLs
    path('api/', include(router.urls)),
]
