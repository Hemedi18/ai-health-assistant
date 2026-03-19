from django.contrib import admin
from .models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'updated_at', 'message_count')
    list_filter = ('created_at', 'updated_at', 'user')
    search_fields = ('user__u_phone_number', 'title')
    readonly_fields = ('id', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_title', 'message_type', 'content_preview', 'created_at')
    list_filter = ('message_type', 'created_at', 'user')
    search_fields = ('user__u_phone_number', 'content')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    def session_title(self, obj):
        return obj.session.title if obj.session else 'No Session'
    session_title.short_description = 'Session'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'
