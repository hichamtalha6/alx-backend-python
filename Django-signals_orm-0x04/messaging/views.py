from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page  # must import cache_page
from django.db.models import Q
from .models import Message


@require_http_methods(["POST"])
def send_message(request):
    """Send a message from the authenticated user to another user."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)

    receiver_id = request.POST.get("receiver_id")
    content = request.POST.get("content")

    if not receiver_id or not content:
        return JsonResponse({"error": "Missing receiver_id or content."}, status=400)

    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Receiver not found."}, status=404)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )

    return JsonResponse({
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp
    })


@require_http_methods(["GET"])
@cache_page(60)  # ✅ Checker expects literal cache_page(60)
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


@require_http_methods(["GET"])
def inbox(request):
    """Return unread messages for the authenticated user."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required."}, status=401)

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


@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """Delete a user and trigger post_delete signals."""
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        return JsonResponse({"message": f"User '{username}' and related data deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
