from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Accounts - includes auth, dashboard, API
    path('accounts/', include('accounts.urls')),
    
    # Chat AI
    path('chat/', include('chat_ai.urls')),
    
    # Menstrual cycle tracking
    path('menstrual/', include('menstrual.urls')),
    
    # Root - redirect to home
    path('', include('accounts.urls')),
]