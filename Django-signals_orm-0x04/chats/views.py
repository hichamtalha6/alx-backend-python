from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message

@cache_page(60)  # ✅ Cache this view for 60 seconds
def get_conversation(request, user_id):
    """Retrieve all messages between request.user and another user."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)

    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver', 'parent_message') \
     .prefetch_related('replies', 'replies__sender', 'replies__receiver') \
     .only('id', 'sender__username', 'receiver__username', 'content', 'timestamp', 'parent_message') \
     .order_by('timestamp')

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "parent": msg.parent_message.id if msg.parent_message else None
        }
        for msg in messages
    ]

    return JsonResponse({"conversation": data})
