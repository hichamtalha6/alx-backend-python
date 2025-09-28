# messaging_app/chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Example: add a derived field with SerializerMethodField
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "sender_username", "content", "timestamp"]

    def validate_content(self, value):
        """
        Custom validation for message content.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message content cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Message is too long (max 500 characters).")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        latest = obj.messages.order_by("-timestamp").first()
        return MessageSerializer(latest).data if latest else None

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "last_message"]
