from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class ChatSession(models.Model):
    """Stores individual chat conversations/sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=200, default='New Chat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.title}"
    
    def get_preview(self):
        """Get first message as preview"""
        message = self.messages.filter(message_type='user').first()
        if message:
            return message.content[:50] + ('...' if len(message.content) > 50 else '')
        return 'Empty chat'


class ChatMessage(models.Model):
    """Stores chat messages between user and AI"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('ai', 'AI'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['session', 'created_at']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.message_type}: {self.content[:50]}"
