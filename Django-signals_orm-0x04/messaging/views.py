from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Message

@require_http_methods(["GET"])
def inbox(request):
    """
    Return unread messages for the authenticated user.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)

    # ✅ Use custom manager method and .only() optimization
    unread_messages = Message.unread.unread_for_user(request.user)

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in unread_messages
    ]
    return JsonResponse({"unread_messages": data})
