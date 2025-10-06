from django.db import models
from django.contrib.auth.models import User


# ✅ Custom Manager to get unread messages efficiently
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for the given user,
        using .only() to select minimal fields for performance.
        """
        return (
            self.filter(receiver=user, read=False)
            .select_related('sender', 'receiver')
            .only('id', 'sender__username', 'content', 'timestamp')
        )


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name='edited_messages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    parent_message = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    # ✅ New field to track if message has been read
    read = models.BooleanField(default=False)

    # ✅ Attach the custom manager
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def get_thread(self):
        """
        Recursively fetch all replies (and nested replies) for this message.
        """
        thread = []
        for reply in self.replies.all().select_related('sender', 'receiver'):
            thread.append({
                "id": reply.id,
                "content": reply.content,
                "sender": reply.sender.username,
                "timestamp": reply.timestamp,
                "replies": reply.get_thread()
            })
        return thread

    @classmethod
    def get_conversation(cls, user):
        """
        Optimized query to get all messages (and replies) in a user's conversations.
        """
        return cls.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user),
            parent_message__isnull=True
        ).select_related('sender', 'receiver').prefetch_related('replies', 'replies__sender', 'replies__receiver')


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message ID {self.message.id} at {self.edited_at}"
