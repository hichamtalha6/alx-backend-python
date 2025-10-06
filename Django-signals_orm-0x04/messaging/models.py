from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # ✅ Track if the message was edited

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class MessageHistory(models.Model):
    """Stores the old content of a message when it's edited."""
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"


# ✅ SIGNAL: Before saving a message, log the old content if it’s being edited
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    If a message is being updated (not created), store its old content
    before the update and mark it as edited.
    """
    if instance.pk:  # Only applies to existing messages
        try:
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return  # New message, ignore

        if old_instance.content != instance.content:
            # Log old content before saving new one
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )
            instance.edited = True
