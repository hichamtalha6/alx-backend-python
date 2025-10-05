from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# In-memory storage for rate limiting
RATE_LIMIT = {}
MAX_MESSAGES = 5  # limit per minute
TIME_WINDOW = timedelta(minutes=1)


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages (POST requests)
    a user can send within a 1-minute window based on their IP address.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only limit POST requests (i.e., sending messages)
        if request.method == "POST":
            ip_address = self.get_client_ip(request)
            now = datetime.now()

            # Get the request history for this IP
            if ip_address not in RATE_LIMIT:
                RATE_LIMIT[ip_address] = []

            # Filter out timestamps older than 1 minute
            RATE_LIMIT[ip_address] = [
                t for t in RATE_LIMIT[ip_address] if now - t < TIME_WINDOW
            ]

            # Check if IP exceeded limit
            if len(RATE_LIMIT[ip_address]) >= MAX_MESSAGES:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1>"
                    "<p>You have exceeded the message limit. Please wait a minute before sending more messages.</p>"
                )

            # Add current request timestamp
            RATE_LIMIT[ip_address].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Retrieve client's IP address (supports proxy headers)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
