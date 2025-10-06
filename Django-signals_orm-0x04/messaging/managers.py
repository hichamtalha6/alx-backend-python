from django.db import models


class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Return unread messages for the given user,
        using .only() to fetch only necessary fields.
        """
        return (
            self.filter(receiver=user, read=False)
            .select_related('sender', 'receiver')
            .only('id', 'sender__username', 'content', 'timestamp')
        )
