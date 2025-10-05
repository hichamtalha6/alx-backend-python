from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the site between certain hours.
    Allows access only between 6:00 PM (18:00) and 9:00 PM (21:00).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Deny access outside 18:00–21:00
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access to the chat is only allowed between 6 PM and 9 PM.</p>"
            )

        # Continue normally during allowed hours
        response = self.get_response(request)
        return response
