# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

# ---------------------------
# Request logging middleware
# ---------------------------
class RequestLoggingMiddleware:
    """Logs each user's requests to requests.log with timestamp, user, and path."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('chats.requests')
        if not self.logger.handlers:
            handler = logging.FileHandler("requests.log")
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = "Anonymous"
        if getattr(request, "user", None) and request.user.is_authenticated:
            user = request.user
        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


# -----------------------------------------
# Access restriction by server time (chat)
# -----------------------------------------
class RestrictAccessByTimeMiddleware:
    """
    Restrict access to chat endpoints outside allowed hours.
    Allowed window: 18:00 (6 PM) <= hour < 21:00 (9 PM).
    This middleware only applies to common chat/message endpoints.
    """
    CHAT_PATH_PREFIXES = ("/api/messages", "/messages", "/chat")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(p) for p in self.CHAT_PATH_PREFIXES):
            now = datetime.now()
            if now.hour < 18 or now.hour >= 21:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1>"
                    "<p>Access to the chat is only allowed between 6 PM and 9 PM.</p>"
                )
        return self.get_response(request)


# -----------------------------------------
# Simple rate-limiting middleware by IP
# -----------------------------------------
_RATE_LIMIT_STORE = {}  # in-memory: { ip_address: [datetime, ...] }
_MAX_MESSAGES = 5
_TIME_WINDOW = timedelta(minutes=1)
RATE_LIMITED_PATH_PREFIXES = ("/api/messages", "/messages", "/chat")

class OffensiveLanguageMiddleware:
    """
    Limits number of POST requests (messages) from an IP to _MAX_MESSAGES per _TIME_WINDOW.
    Returns 403 when exceeded.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and any(request.path.startswith(p) for p in RATE_LIMITED_PATH_PREFIXES):
            ip = self.get_client_ip(request) or "unknown"
            now = datetime.now()
            timestamps = _RATE_LIMIT_STORE.get(ip, [])
            # keep only recent timestamps within the time window
            timestamps = [t for t in timestamps if now - t < _TIME_WINDOW]
            if len(timestamps) >= _MAX_MESSAGES:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1>"
                    "<p>You have exceeded the message limit. Please wait a minute before sending more messages.</p>"
                )
            timestamps.append(now)
            _RATE_LIMIT_STORE[ip] = timestamps
        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """Support proxied headers (X-Forwarded-For) if present, else REMOTE_ADDR."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


# -----------------------------------------
# Role-based permission middleware
# -----------------------------------------
class RolepermissionMiddleware:
    """
    Enforces that certain restricted actions/paths are accessible only by admin or moderator.
    - Only checks a small set of 'restricted' path prefixes (adjust as needed).
    - Considers user.is_superuser or user.is_staff as admin/moderator OR a custom user.role field.
    """
    RESTRICTED_PATH_PREFIXES = (
        "/api/admin",
        "/api/messages/moderate",
        "/api/messages/delete",
        "/admin",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only evaluate for restricted paths
        if any(request.path.startswith(p) for p in self.RESTRICTED_PATH_PREFIXES):
            user = getattr(request, "user", None)
            # require authentication first
            if not user or not user.is_authenticated:
                return HttpResponseForbidden(
                    "<h1>403 Forbidden</h1><p>You must be logged in to access this resource.</p>"
                )

            # Accept if Django admin/staff flags are set
            if user.is_superuser or user.is_staff:
                return self.get_response(request)

            # Or accept if user has a custom role attribute set to admin/moderator
            role = getattr(user, "role", None)
            if role in ("admin", "moderator"):
                return self.get_response(request)

            # Otherwise deny
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access denied: Admin or Moderator role required.</p>"
            )

        # Non-restricted path: continue normally
        return self.get_response(request)
