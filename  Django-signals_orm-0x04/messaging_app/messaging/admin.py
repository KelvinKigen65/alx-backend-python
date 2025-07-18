from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Message model.
    """
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')
    readonly_fields = ('timestamp',) # Timestamp is auto_now_add

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Notification model.
    """
    list_display = ('user', 'message', 'is_read', 'timestamp')
    list_filter = ('is_read', 'timestamp', 'user')
    search_fields = ('user__username', 'message__content')
    raw_id_fields = ('message', 'user') # For large numbers of messages/users, show raw IDs
    readonly_fields = ('timestamp',) # Timestamp is auto_now_add
