from django.contrib import messages
from django.contrib.auth import logout
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


class RemoveNoindexHeaderMiddleware:
    """
    Workaround middleware to remove X-Robots-Tag: noindex header set by Traefik/Pangolin.

    This allows Google to index public pages while keeping the proxy configuration as-is.
    Only removes the header for public (non-admin, non-accounts) pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only modify responses for public pages (not admin, not accounts)
        path = request.path
        is_public = not any(
            [
                path.startswith("/admin/"),
                "/accounts/" in path,
            ]
        )

        if is_public and "X-Robots-Tag" in response:
            # Remove the noindex header set by the proxy
            del response["X-Robots-Tag"]

        return response
