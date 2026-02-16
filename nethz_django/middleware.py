from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class SEORedirectMiddleware:
    """
    SEO-friendly redirect middleware.

    Handles:
    - Root URL: redirect "/" to the best-fit language (de/en) with 302 (temporary),
      because the target depends on cookies / Accept-Language and is not permanent.
    - Trailing slash: redirect "/path" -> "/path/" with 301 for GET requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_prefixes = ("/admin/", "/assets/", "/static/")

    def __call__(self, request):
        path = request.path
        chosen_lang = None

        # If user visits a language-prefixed URL, persist that choice (session + cookie)
        # Supports /de/, /de, /en/, /en/anything...
        for lang_code, _lang_name in settings.LANGUAGES:
            prefix = f"/{lang_code}"
            if path == prefix or path.startswith(prefix + "/"):
                session_obj = getattr(request, "session", None)
                if session_obj is not None:
                    session_obj[settings.LANGUAGE_COOKIE_NAME] = lang_code
                chosen_lang = lang_code
                break

        # Root URL: redirect to best-fit language with 302 (temporary)
        # A 302 is correct here because the redirect target depends on the
        # user's cookie / Accept-Language, so it is not truly permanent.
        # Using 301 caused Google to report "Umleitungsfehler" (redirect error)
        # because it caches 301s aggressively and cannot handle a permanent
        # redirect whose target varies by cookie state.
        if path == "/":
            # 1) honor persisted choice (cookie or session)
            lang_cookie = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            session_obj = getattr(request, "session", None)
            lang_session = (
                session_obj.get(settings.LANGUAGE_COOKIE_NAME) if session_obj else None
            )
            user_language = lang_cookie or lang_session
            # 2) fallback to Accept-Language
            if not user_language:
                user_language = translation.get_language_from_request(
                    request, check_path=False
                )
            supported = [lang[0] for lang in settings.LANGUAGES]
            if user_language not in supported:
                user_language = settings.LANGUAGE_CODE
            response = HttpResponseRedirect(f"/{user_language}/")
            if user_language:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, user_language, max_age=31536000
                )
            return response

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
            response = HttpResponsePermanentRedirect(new_path)
            if chosen_lang:
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME, chosen_lang, max_age=31536000
                )
            return response

        response = self.get_response(request)

        # Persist chosen language on normal responses too
        if chosen_lang and response:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, chosen_lang, max_age=31536000
            )

        return response


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
