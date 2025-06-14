from django.apps import AppConfig

class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'
    verbose_name = 'Messaging and Notifications'

    def ready(self):
        """
        Import signals when the app is ready.
        This ensures that signal handlers are connected when Django starts.
        Add a print statement here to confirm this method is called.
        """
        print("MessagingConfig ready() called - Attempting to import signals.")
        import messaging # noqa: F401
        # The noqa: F401 comment is to suppress the 'imported but unused' warning,
        # as importing signals is for their side effects (connecting to senders).
