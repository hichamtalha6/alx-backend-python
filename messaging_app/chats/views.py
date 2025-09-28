# messaging_app/chats/views.py
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username", "participants__email"]
    ordering_fields = ["conversation_id"]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant IDs.
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "A conversation requires at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"error": "One or more participant IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["content", "sender__username"]
    ordering_fields = ["timestamp"]

    def create(self, request, *args, **kwargs):
        """
        Send a new message in an existing conversation.
        Requires: sender_id, conversation_id, content.
        """
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        content = request.data.get("content")

        if not sender_id or not conversation_id or not content:
            return Response(
                {"error": "sender_id, conversation_id, and content are required."},
