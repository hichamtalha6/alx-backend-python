from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    """
    View that allows a user to delete their account.
    """
    try:
        user = User.objects.get(id=user_id)
        username = user.username
        user.delete()
        return JsonResponse({"message": f"User '{username}' and related data deleted successfully."})
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
