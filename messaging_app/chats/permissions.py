# chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.IsAuthenticated):
    """
    Custom permission:
    - Only authenticated users can access
    - Only participants in a conversation can view, send, update, or delete messages
    """

    def has_object_permission(self, request, view, obj):
        # If object is a Conversation, check participants
        if hasattr(obj, "participants"):  # Conversation model
            return request.user in obj.participants.all()

        # If object is a Message, check participants of the related conversation
        if hasattr(obj, "conversation"):  # Message model
            return request.user in obj.conversation.participants.all()

        return False
