from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a notification when a new Message instance is saved.
    Added more detailed print statements for debugging the creation process.
    """
    # Print at the very start of the signal to confirm it's triggered
    print(f"DEBUG: Signal 'create_notification_on_new_message' triggered. Message ID: {instance.id}, Created: {created}")

    if created: # Only create a notification if a new message was created (not updated)
        # Print to confirm we enter the 'created' block
        print(f"DEBUG: Message was newly created. Attempting to create notification for receiver: {instance.receiver.username if instance.receiver else 'None'}")

        # Ensure the receiver user exists before trying to create a notification for them
        if instance.receiver:
            try:
                # Attempt to create the notification
                notification = Notification.objects.create(
                    user=instance.receiver,
                    message=instance,
                    is_read=False # New notifications are unread by default
                )
                # Print upon successful creation, including the new notification's ID
                print(f"DEBUG: Notification successfully created! Notification ID: {notification.id}, User: {notification.user.username}, Message: {notification.message.id}")
            except Exception as e:
                # Catch any errors during notification creation and print them
                print(f"ERROR: Failed to create notification for receiver {instance.receiver.username}. Error: {e}")
        else:
            # Print if the receiver is unexpectedly null
            print(f"DEBUG: Could not create notification: Message receiver for message ID {instance.id} is null.")
    else:
        # Print if the message was updated, not created
        print(f"DEBUG: Message was updated (created=False). Skipping notification creation.")

