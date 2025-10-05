from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware that restricts access based on user role.
    Only users with 'admin' or 'moderator' roles can access certain actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        user = request.user

        # You can modify this condition depending on your app's user model
        # For simplicity, we assume "is_staff" or "is_superuser" = admin/moderator
        if not user.is_authenticated:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>You must be logged in to access this resource.</p>"
            )

        # Check role permissions
        if not (user.is_superuser or user.is_staff):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Access denied: Admin or Moderator role required.</p>"
            )

        # Allow request to continue
        response = self.get_response(request)
        return response
