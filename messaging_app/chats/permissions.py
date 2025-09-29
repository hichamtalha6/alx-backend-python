# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(IsAuthenticated):
    """
    Allow only authenticated users who are participants of a conversation
    """
    def has_object_permission(self, request, view, obj):
        # obj is either a Conversation or a Message
        if hasattr(obj, "participants"):  # Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, "conversation"):  # Message
            return request.user in obj.conversation.participants.all()
        return False
