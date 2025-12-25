from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponsePermanentRedirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class SEORedirectMiddleware:
    """
    SEO-friendly redirects with permanent 301 status codes.

    Handles:
    - Root URL: redirect "/" to the best-fit language (default de/en) with 301
    - Trailing slash: redirect "/path" -> "/path/" with 301 for GET requests
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_prefixes = ("/admin/", "/assets/", "/static/")

    def __call__(self, request):
        path = request.path

        # Root URL: override LocaleMiddleware's 302 with a permanent 301
        if path == "/":
            user_language = translation.get_language_from_request(
                request, check_path=False
            )
            supported = [lang[0] for lang in settings.LANGUAGES]
            if user_language not in supported:
                user_language = settings.LANGUAGE_CODE
            return HttpResponsePermanentRedirect(f"/{user_language}/")

        # Enforce trailing slash for safe methods (GET/HEAD)
        if (
            request.method in ("GET", "HEAD")
            and not path.endswith("/")
            and not path.startswith(self.excluded_prefixes)
            and "." not in path.split("/")[-1]
        ):
            new_path = path + "/"
            if request.META.get("QUERY_STRING"):
                new_path += "?" + request.META["QUERY_STRING"]
            return HttpResponsePermanentRedirect(new_path)

        return self.get_response(request)


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
