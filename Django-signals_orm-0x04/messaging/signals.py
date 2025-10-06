from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Automatically create a notification when a new message is sent."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Before saving a message, log its old content if edited."""
    if instance.pk:
        try:
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return

        if old_instance.content != instance.content:
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Automatically clean up related data when a User is deleted.
    """
    # ✅ Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # ✅ Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # ✅ Delete message histories related to that user’s messages
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
