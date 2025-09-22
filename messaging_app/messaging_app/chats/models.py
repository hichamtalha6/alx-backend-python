import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Uses UUID as primary key and adds extra fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(default=timezone.now)

    # Remove username requirement since we use email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    """
    Conversation model representing a chat between multiple users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"


class Message(models.Model):
    """
    Message model linked to a conversation and sender.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.id} from {self.sender.email}"
