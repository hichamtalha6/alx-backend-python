from datetime import datetime
from django.http import HttpResponseForbidden
import logging


class RequestLoggingMiddleware:
    """Logs each user’s requests to a file with timestamp, user, and path."""

    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access outside allowed hours.
    Allows access only between 6 PM (18:00) and 9 PM (21:00).
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

        response = self.get_response(request)
        return response
