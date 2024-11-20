from datetime import timedelta, datetime
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages


# class AutoLogoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             last_activity = request.session.get("last_activity")

#             if last_activity:
#                 last_activity = datetime.fromisoformat(last_activity)

#                 if timezone.is_naive(last_activity):
#                     last_activity = timezone.make_aware(last_activity)

#                 time_diff = timezone.now() - last_activity

#                 if time_diff > timedelta(minutes=50):
#                     messages.info(
#                         request, "Tu sesión ha expirado debido a inactividad."
#                     )
#                     logout(request)
#                     return redirect("login:loginapps")

#             request.session["last_activity"] = timezone.now().isoformat()

#         response = self.get_response(request)
#         return response
