import functools

from django.http import JsonResponse

def is_user_logged_in(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You need to log in to view popular movies"}, status=403)  # Forbidden
        return view_func(self, request, *args, **kwargs)
    return wrapper