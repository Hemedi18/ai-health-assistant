"""Menstrual cycle tracking URLs"""
from django.urls import path
from . import views

app_name = 'menstrual'

urlpatterns = [
    # Main pages (form-based)
    path('', views.dashboard_view, name='dashboard'),
    path('setup/', views.setup_view, name='setup'),
    
    # API endpoints (kept for charts/data fetching only)
    path('api/cycle-info/', views.get_cycle_info, name='cycle_info'),
    path('api/logs/', views.get_daily_logs, name='cycle_logs'),
    path('api/guidance/', views.get_guidance, name='guidance'),
    path('api/cycle-diagram/', views.get_cycle_diagram_data, name='cycle_diagram'),
]
