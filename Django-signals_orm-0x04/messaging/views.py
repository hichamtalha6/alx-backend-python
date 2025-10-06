from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """
    View that allows a user to delete their account.
    """
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        return JsonResponse({"message": f"User '{username}' and related data deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)


# ✅ SIGNAL: Automatically clean up related data when a user is deleted
@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    When a User is deleted, remove all messages, notifications,
    and message histories associated with that user.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories related to messages that belonged to this user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
