from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='12345')
        self.receiver = User.objects.create_user(username='receiver', password='12345')

    def test_notification_created_on_message(self):
        """Test that a notification is automatically created when a new message is sent."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello there!"
        )

        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.is_read)
