# chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants in a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Restrict access to conversation participants.
        Handle safe methods (GET, HEAD, OPTIONS) and unsafe (POST, PUT, PATCH, DELETE).
        """

        # If object is a Conversation
        if hasattr(obj, "participants"):  
            return request.user in obj.participants.all()

        # If object is a Message
        if hasattr(obj, "conversation"):  
            is_participant = request.user in obj.conversation.participants.all()

            # Allow viewing messages if participant
            if request.method in permissions.SAFE_METHODS:
                return is_participant

            # For modification (PUT, PATCH, DELETE), must be sender
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return is_participant and obj.sender == request.user

            # For creating messages (POST), must be participant
            if request.method == "POST":
                return is_participant

        return False
