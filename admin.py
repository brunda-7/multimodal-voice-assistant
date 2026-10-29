from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created_at', 'message_count']
    list_filter = ['created_at', 'user']
    search_fields = ['title', 'user__username']
    inlines = [MessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'content_preview', 'is_user', 'timestamp']
    list_filter = ['is_user', 'timestamp', 'conversation']
    search_fields = ['content', 'conversation__title']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'