# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter messages by start and end timestamp
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    # Filter by sender
    sender_id = django_filters.UUIDFilter(field_name="sender__user_id")
    # Filter by conversation
    conversation_id = django_filters.UUIDFilter(field_name="conversation__conversation_id")

    class Meta:
        model = Message
        fields = ["sender_id", "conversation_id", "start_date", "end_date"]
