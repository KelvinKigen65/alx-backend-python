
from django.db import models
from django.contrib.auth.models import User # Assuming Django's built-in User model

class Message(models.Model):
    """
    Represents a private message sent between users.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp'] # Order messages by most recent first

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    """
    Represents a notification for a user, typically triggered by an event like a new message.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    # The message field is optional because a notification might be for something other than a message,
    # though for this specific task, it will always be linked to a message.
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    # A generic content field can be added if notifications are to be more versatile
    # content = models.CharField(max_length=255, default="New message received")

    class Meta:
        ordering = ['-timestamp'] # Order notifications by most recent first

    def __str__(self):
        status = "read" if self.is_read else "unread"
        if self.message:
            return f"Notification for {self.user.username}: New message from {self.message.sender.username} ({status})"
        return f"Notification for {self.user.username} ({status})"
