from django.contrib.auth import logout
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_email_verified:
            messages.warning(
                request, _("You have to confirm your email address to log in.")
            )
            logout(request)

        response = self.get_response(request)
        return response
