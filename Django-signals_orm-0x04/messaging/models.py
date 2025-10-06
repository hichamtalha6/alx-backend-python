from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

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
    read = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    def get_thread(self):
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
        return cls.objects.filter(
            models.Q(sender=user) | models.Q(receiver=user),
            parent_message__isnull=True
        ).select_related('sender', 'receiver').prefetch_related('replies', 'replies__sender', 'replies__receiver')
