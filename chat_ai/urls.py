from django.urls import path
from . import views

urlpatterns = [
    # Serve the chat interface at the base '/chat/' URL
    path('', views.chat_view, name='chat_interface'),
    # Intro / landing page moved to /chat/intro/
    path('intro/', views.chat_home, name='chat_home'),
    path('api/send/', views.chat_api, name='chat_api'),
    path('api/history/', views.get_chat_history, name='chat_history'),
    path('api/sessions/<str:session_id>/', views.get_session_messages, name='session_messages'),
    path('api/new-session/', views.create_new_session, name='new_session'),
    path('api/delete-session/<str:session_id>/', views.delete_session, name='delete_session'),
    
    # AI Health Features API
    path('api/health-summary/', views.health_summary_view, name='health_summary'),
    path('api/symptom-assess/', views.symptom_assessment_view, name='symptom_assess'),
    path('api/disclaimer/', views.health_disclaimer_view, name='health_disclaimer'),
    path('api/ask-question/', views.ask_health_question_view, name='ask_question'),
    path('api/nutrition-advice/', views.nutrition_advice_view, name='nutrition_advice'),
    path('api/wellness-tips/', views.wellness_tips_view, name='wellness_tips'),
    path('api/exercise-recommendations/', views.exercise_recommendations_view, name='exercise_recommendations'),
]
